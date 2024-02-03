from pydantic import BaseModel


class SourceModel(BaseModel):
    source: str
    secret_key: str


class QuestionModel(BaseModel):
    question: str
    session_id: str 