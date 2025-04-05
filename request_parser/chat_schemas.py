from pydantic import BaseModel
from uuid import UUID
# from llama_index.core.llms import ChatMessage
from datetime import datetime

class SourceModel(BaseModel):
    source: str
    data_type: str
    secret_key: str


class QuestionModel(BaseModel):
    question: str
    session_id: str

class SessionData(BaseModel):
    time_created : datetime
    chat_history : list