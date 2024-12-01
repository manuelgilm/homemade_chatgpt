from pydantic import BaseModel
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import Field


class Message(BaseModel):
    text: str
    creator: str
    created_at: datetime = Field(default=datetime.now())
    reactions: Optional[List[str]] = []


class ChatHistory(BaseModel):
    messages: List[Message]
