from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Field
from typing import List
from sqlmodel import SQLModel
from sqlmodel import Relationship
import uuid
from typing import Optional
from src.api.db.models.user import User


class Message(BaseModel):
    text: str
    creator: str
    created_at: datetime = Field(default=datetime.now())


class Interaction(BaseModel):
    messages: List[Message]
    started_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class Chat(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True)
    name: str = Field(index=True, max_length=50)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    def __repr__(self):
        return f"<Chat {self.name}>"
