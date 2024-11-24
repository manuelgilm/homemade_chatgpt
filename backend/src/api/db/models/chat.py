from pydantic import BaseModel
from datetime import datetime 
from sqlmodel import Field
from typing import List 

class Message(BaseModel):
    text: str
    creator: str
    created_at: datetime = Field(default=datetime.now())

class Interaction(BaseModel):
    messages: List[Message]
    started_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
