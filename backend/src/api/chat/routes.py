from fastapi import APIRouter
from fastapi import Depends
from src.api.resources.chat_manager import ChatManager
from src.api.chat.schemas import ChatCreateSchema
from src.api.db.main import get_session

chat_router = APIRouter(tags=["chat"])


# Create Chat
@chat_router.post("/create")
async def create_chat(
    chat_data: ChatCreateSchema,
    chat_manager: ChatManager = Depends(ChatManager),
    session=Depends(get_session),
):
    chat_name = chat_data.name
    chat_exists = chat_manager.chat_exists(name=chat_name, session=session)
    if chat_exists:
        return {"detail": "Chat already exists"}
    new_chat = chat_manager.create_chat(session=session, chat_data=chat_data)
    return new_chat.model_dump()


# Get Chat
@chat_router.get("/{chat_id}")
async def get_chat(chat_id: int):
    pass


# Get All Chats
@chat_router.get("/all")
async def get_all_chats():
    pass


# Update Chat
@chat_router.put("/{chat_id}")
async def update_chat(chat_id: int):
    pass


# Delete Chat
@chat_router.delete("/{chat_id}")
async def delete_chat(chat_id: int):
    pass
