from pydantic import BaseModel


class ChatCreateSchema(BaseModel):
    name: str
    user_id: str
