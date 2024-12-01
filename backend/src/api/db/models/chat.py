from src.api.resources.llm_core.data_models import ChatHistory
from datetime import datetime
from sqlmodel import Field
from typing import List
from sqlmodel import SQLModel
import uuid
from typing import Optional


class Chat(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True)
    name: str = Field(index=True, max_length=50)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    def __repr__(self):
        return f"<Chat {self.name}>"


class ChatSession(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True)
    chat_id: uuid.UUID = Field(foreign_key="chat.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    chat_history: List[ChatHistory]

    def __repr__(self):
        return f"<ChatSession {self.id}>"
