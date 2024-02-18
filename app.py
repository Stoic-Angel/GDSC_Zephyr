from fastapi import FastAPI, responses, Header, HTTPException, Depends
from settings import Settings
from request_parser.chat_schemas import SourceModel, QuestionModel
from settings import Settings
from dataset.final_datas import final_datas
from models.zephyr import zephyr_model

app = FastAPI(title=f"{Settings.PROJECT_NAME} API",
              version=Settings.PROJECT_VERSION)


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
        students related to GDSC JSSATEN chapter. You should answer strictly to training dataset. If you do not know the answer
        to query or question, just reply \"Sorry, I didn't get that. You can try contacting GDSC members directly from https://gdscjss.in/team\".
        You are expert in all coding languages."""
    ]
    prompt_parts.extend(final_datas)
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
