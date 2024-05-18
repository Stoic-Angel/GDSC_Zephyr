from pydantic import BaseModel
from uuid import UUID
from llama_index.core.llms import ChatMessage

class SourceModel(BaseModel):
    source: str
    data_type: str
    secret_key: str


class QuestionModel(BaseModel):
    question: str
    session_id: UUID

class SessionData(BaseModel):
    # session_id : str
    chat_history : list