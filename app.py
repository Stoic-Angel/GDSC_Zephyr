from fastapi import FastAPI, responses

from embedchain import Pipeline
from request_parser.chat_schemas import SourceModel, QuestionModel
from settings import Settings

app = FastAPI(title=f"{Settings.PROJECT_NAME} API", version=Settings.PROJECT_VERSION)
embedchain_app = Pipeline()




@app.post("/add")
async def add_source(source_model: SourceModel):

    if source_model.secret_key != Settings.SECRET_KEY:
        return {"message": "Invalid secret key."}
    
    source = source_model.source
    embedchain_app.add(source, data_type="text")

    return {"message": f"Source '{source}' added successfully."}


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
    response = embedchain_app.chat(question, session_id=question_model.session_id)
    return {"response": response}


@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
