from fastapi import FastAPI, responses, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from request_parser.chat_schemas import SourceModel, QuestionModel, SessionData
from settings import Settings
from dataset.database import index
from models.zephyr import get_prompt, zephyr_qa_prompt, get_model

from llama_index.core.llms import ChatMessage


app = FastAPI(title=f"{Settings.PROJECT_NAME} API",
              version=Settings.PROJECT_VERSION)

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


from uuid import uuid4
from session import backend, cookie
from fastapi import Response

@app.post("/create_chat")
async def create_chat(response: Response):
    session = uuid4()
    chat = []
    chat.append(ChatMessage(role="system", content = zephyr_qa_prompt))
    data = SessionData(chat_history=chat)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)
    return { "session_id": session }, 200


@app.post("/chat")
async def handle_chat(question_model: QuestionModel, api_key: str = Depends(get_api_key)):
    question = question_model.question
    session = question_model.session_id
    llm = get_model()

    try:
        session_data = await backend.read(session)
        chat = session_data.chat_history
    except :
        return {"error": "No session found"}, 500
    
    retriever = get_retriever(index)
    context = retriever.retrieve(question)
    chat.append(ChatMessage(role="user", content = get_prompt(context[0].text, question)))

    try:
        response = llm.chat(chat)
        resp = str(response.message)[10:]
        chat.append(ChatMessage(role="assistant", content = resp))
        await backend.update(session, session_data)
        return {"answer": resp}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
