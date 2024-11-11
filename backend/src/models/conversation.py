from pydantic import BaseModel  
from sqlmodel import Field
from sqlmodel import SQLModel
from datetime import datetime 

from typing import List

class Message(BaseModel):
    id_: int
    conversation_id: int
    author: str
    message: str
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())

class ConversationHistory(BaseModel):
    conversation_id: int
    messages: List[Message]
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())
    

class Conversation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    user_id: int
    messages: List[ConversationHistory]
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())