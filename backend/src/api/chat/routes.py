from fastapi import APIRouter
from fastapi import Depends
from typing import Dict
from src.api.auth.dependencies import AccessTokenBearer
from src.api.resources.chat_manager import ChatManager
from src.api.chat.schemas import ChatCreateSchema
from src.api.db.main import get_session

from src.api.resources.llm_core.data_models import Message
from src.api.resources.chat_manager import ChatManager

# from src.api.resources.chat_manager import ChatSessionManager

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


# Delete Chat
@chat_router.delete("/{chat_name}")
async def delete_chat(
    chat_name: str,
    session: Session = Depends(get_session),
    chat_manager: ChatManager = Depends(ChatManager),
):
    chat = chat_manager.get_chat_by_name(chat_name=chat_name, session=session)
    if not chat:
        return {"detail": "Chat not found"}
    result = chat_manager.delete_chat_by_name(session=session, chat_name=chat_name)
    return result


@chat_router.post("/chat-session/{chat_id}")
async def create_chat_session(
    chat_id: str,
    session: Session = Depends(get_session),
    chat_manager: ChatManager = Depends(ChatManager),
    user_details: Dict = Depends(access_token_bearer),
):
    pass
