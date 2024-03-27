from fastapi import FastAPI, responses, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from settings import Settings
from request_parser.chat_schemas import SourceModel, QuestionModel
from settings import Settings
from dataset.final_datas import final_datas
from dataset.final_members import final_members
from models.zephyr import zephyr_model
import pandas as pd

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

final_data = []
df = pd.read_excel("dataset/final_llm_data.xlsx")
for i in range(len(df)):
    final_data.append(f"input: {df.iloc[i, 0]}")
    final_data.append(f"output: {df.iloc[i, 1]}")



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
        You are a virtual AI assistance named Zephyr (exclusive to GDSC JSSATEN) whose job is to clear the doubts of 
        students related to GDSC JSSATEN club. You should answer strictly to given input/output example dataset. Please make sure that your reply should
        not exceed 100 words. Please make sure your response should reflect the tone of AI assisstance Zephyr. If you do not know the answer
        to query or question, just reply \"Sorry, I didn't get that. You can try contacting GDSC members directly from https://gdscjss.in/team\"
        """
    ]
    # prompt_parts.extend(final_datas)
    # prompt_parts.extend(final_members)
    prompt_parts.extend(final_data)
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
