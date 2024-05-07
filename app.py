from fastapi import FastAPI, responses, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from request_parser.chat_schemas import SourceModel, QuestionModel
from settings import Settings
from dataset.database import index
from models.zephyr import zephyr_qa_prompt_template

app = FastAPI(title=f"{Settings.PROJECT_NAME} API",
              version=Settings.PROJECT_VERSION)

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


def get_query_engine(index):
    query_engine = index.as_query_engine(
    similarity_top_k=2,
    verbose=True
  )
    query_engine.update_prompts(
        {"response_synthesizer:text_qa_template":zephyr_qa_prompt_template}
    )

    return query_engine



@app.post("/chat")
async def handle_chat(question_model: QuestionModel, api_key: str = Depends(get_api_key)):

    question = question_model.question
    query_engine = get_query_engine(index)
    try:
        response = query_engine.query(question)
        return {"answer": response}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
