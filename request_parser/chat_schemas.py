from pydantic import BaseModel


class SourceModel(BaseModel):
    source: str
    data_type: str
    secret_key: str


class QuestionModel(BaseModel):
    question: str
    session_id: str = None
