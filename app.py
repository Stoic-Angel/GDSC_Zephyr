from fastapi import FastAPI, responses

from request_parser.chat_schemas import SourceModel, QuestionModel
from settings import Settings
from dataset.final_datas import final_datas
from models.gemini import zephyr_model

app = FastAPI(title=f"{Settings.PROJECT_NAME} API",
              version=Settings.PROJECT_VERSION)


# @app.post("/add")
# async def add_source(source_model: SourceModel):

#     if source_model.secret_key != Settings.SECRET_KEY:
#         return {"message": "Invalid secret key."}

#     source = source_model.source
#     embedchain_app.add(source, data_type=source_model.data_type)

#     return {"message": f"Source '{source}' added successfully."}


# @app.post("/query")
# async def handle_query(question_model: QuestionModel):
#     """
#     Handles a query to the EmbedChain app.
#     Expects a JSON with a "question" key.
#     """
#     question = question_model.question
#     answer = embedchain_app.query(question)
#     return {"answer": answer}


@app.post("/chat")
async def handle_chat(question_model: QuestionModel):

    question = question_model.question
    prompt_parts = [
        "You are a virtual AI assistance named Zypher (exclusive to GDSC JSSATEN) whose job is to clear the doubts of students related to GDSC JSSATEN chapter. You should answer strictly to training dataset. If you do not know the answer to query or question, just reply \"Sorry, I didn't get that. You can try contacting GDSC members directly from https://gdscjss.in/team\". You reply should not exceed more than 50 words.",
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
