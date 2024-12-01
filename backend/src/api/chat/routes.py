from fastapi import APIRouter
from fastapi import Depends
from typing import Dict
from src.api.auth.dependencies import AccessTokenBearer
from src.api.resources.chat_manager import ChatManager
from src.api.chat.schemas import ChatCreateSchema
from src.api.db.main import get_session
from sqlmodel import Session
import uuid

chat_router = APIRouter(tags=["chat"])
access_token_bearer = AccessTokenBearer()


# Create Chat
@chat_router.post("/create")
async def create_chat(
    chat_data: ChatCreateSchema,
    chat_manager: ChatManager = Depends(ChatManager),
    session: Session = Depends(get_session),
    user_details: Dict = Depends(access_token_bearer),
):
    print("User Details: ", user_details)
    chat_name = chat_data.name
    chat_exists = chat_manager.chat_exists(name=chat_name, session=session)
    if chat_exists:
        return {"detail": "Chat already exists"}

    new_chat = chat_manager.create_chat(
        session=session,
        chat_data={
            "name": chat_name,
            "user_id": uuid.UUID(user_details["user"]["user_uid"]),
        },
    )
    return new_chat.model_dump()


# # Get Chat
# @chat_router.get("/{chat_id}")
# async def get_chat(chat_id: int):
#     pass


# Get All Chats
@chat_router.get("/all")
async def get_all_chats(
    session: Session = Depends(get_session),
    chat_manager: ChatManager = Depends(ChatManager),
    user_details: Dict = Depends(access_token_bearer),
):
    print("User Details: ", user_details)
    chats = chat_manager.get_all_chats_user(
        session=session, user_id=user_details["user"]["user_uid"]
    )
    print("Chats: ", chats)
    if chats:
        return [chat.model_dump() for chat in chats]
    return {"detail": "No chats found"}


# # Update Chat
# @chat_router.put("/{chat_id}")
# async def update_chat(chat_id: int):
#     pass


# # Delete Chat
# @chat_router.delete("/{chat_id}")
# async def delete_chat(chat_id: int):
#     pass
