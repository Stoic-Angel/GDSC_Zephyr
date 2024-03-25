from fastapi import FastAPI, responses, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from settings import Settings
from request_parser.chat_schemas import SourceModel, QuestionModel
from settings import Settings
from dataset.final_datas import final_datas
from dataset.final_members import final_members
from models.zephyr import zephyr_model

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


@app.post("/chat")
async def handle_chat(question_model: QuestionModel, api_key: str = Depends(get_api_key)):

    question = question_model.question
    prompt_parts = [
        """
        You are a virtual AI assistant named Zephyr whose job is to clear the doubts of 
        students related to the GDSC club of JSSATEN or contemporary technology in a concise manner. Try to answer queries related to any 
        technology based on your knowledge from the internet. If the query is related to GDSC, answer from 
        the dataset I've provided. Try to limit your response to 100 words. If you do not know the answer
        to any question, just reply with this: \"Sorry, I didn't get that. You can try contacting GDSC members directly from https://gdscjss.in/team\"
        """
    ]
    prompt_parts.extend(final_datas)
    prompt_parts.extend(final_members)
    prompt_parts.append("input: " + question)
    prompt_parts.append("output:")
    try:
        response = zephyr_model.generate_content(prompt_parts)
        return {"answer": response.text}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
