from fastapi import FastAPI, responses, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from request_parser.chat_schemas import SourceModel, QuestionModel, SessionData
from settings import Settings
from dataset.database import index
from models.zephyr import get_prompt, zephyr_qa_prompt, get_model, tools
import json
import asyncio
import contextlib
from datetime import datetime, timedelta, UTC

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.DEBUG, force=True)
logger = logging.getLogger("uvicorn")

file_handler = RotatingFileHandler("app.log", maxBytes=5 * 1024 * 1024, backupCount=3)
logger.addHandler(file_handler)

log_format = "%(asctime)s - %(levelname)s - %(message)s"
for handler in logger.handlers:
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(log_format))

logger.setLevel(logging.DEBUG)

from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Launch an async task to clean expired sessions periodically."""

    async def cleanup():
        while True:
            now = datetime.now(UTC)
            expired_tokens = [
                token for token, data in backend.data.items()
                if (now - data.time_created) > timedelta(hours=Settings.SESSION_EXPIRY)
            ]
            if expired_tokens:
                await asyncio.gather(*(backend.delete(token) for token in expired_tokens))
            await asyncio.sleep(3600)

    cleanup_task = asyncio.create_task(cleanup())
    yield 
    cleanup_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await cleanup_task

app = FastAPI(title=f"{Settings.PROJECT_NAME} API",
              version=Settings.PROJECT_VERSION, lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_api_key(authorization: str = Header(...)):
    expected_key = Settings.SECRET_KEY
    if authorization != f"Bearer {expected_key}":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return authorization


def get_retriever(index):
    retriever = index.as_retriever(similarity_top_k=2)
    return retriever


def get_info_from_docs(query: str) -> str:
    """Get information about GDG OnCampus JSSATEN and it's members and the events in conducts. Whenever asked about people using their names, use this tool. Whenever asked about GDSC events, use this tool. DONT use the tool when the question is not related to GDSC or it is a general question."""
    retriever = get_retriever(index)
    context = retriever.retrieve(query)
    return context[0].text


from uuid import uuid4
from session import backend, cookie
from fastapi import Response

@app.get("/create_chat")
async def create_chat(_: str = Depends(get_api_key)):
    session = uuid4()
    chat = []
    chat.append({"role": "system", "content":zephyr_qa_prompt})
    data = SessionData(time_created=datetime.now(UTC), chat_history=chat)

    await backend.create(session, data)
    logger.debug(f"Session created sucessfully for ID: {session} at time: {datetime.now(UTC)}")

    return { "session_id": session }, 200


@app.post("/chat")
async def handle_chat(question_model: QuestionModel):
    question = question_model.question
    session = question_model.session_id

    logger.debug("Fetching LLM")
    llm = get_model()

    if not llm:
        return {"error": "An error occurred. Please try again later!"}, 500

    try:
        session_data = await backend.read(session)
        logger.debug(f"Session fetched successfully for ID: {session}")
        chat = session_data.chat_history
    except :
        logger.debug(f"Error fetching session for ID: {session}")
        return {"error": "No session found"}, 500
    
    chat.append({"role": "user", "content": question})

    logger.debug(f"Requesting response for messages: {chat}")
    response = llm.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = chat,
        tools = tools
        )
    resp = response.choices[0].message
    chat.append(resp)
    tool_calls = resp.tool_calls
    
    try:
        if tool_calls:
            logger.debug(f"Tool call detected: {tool_calls}")
            for tool_call in tool_calls:
                function_args = json.loads(tool_call.function.arguments)
                func_resp = get_info_from_docs(function_args.get("query"))
                logger.debug(f"Tool response: {func_resp}")
                chat.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_info_from_docs",
                    "content": func_resp,
                })

                response = llm.chat.completions.create(
                    model = "gpt-3.5-turbo-0125",
                    messages = chat
                )
                resp = response.choices[0].message

        await backend.update(session, session_data)
        logger.debug(f"Returning LLM response: {resp.content}")

        return {"answer": resp.content}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
