from fastapi import Depends
from sqlmodel import Session
from typing import Dict
from typing import Any
from src.api.db.models.chat import Chat
from src.api.chat.schemas import ChatCreateSchema
from sqlmodel import select
from typing import Optional
import uuid


class ChatManager:

    def create_chat(self, session: Session, chat_data: Dict) -> Chat:

        new_chat = Chat(**chat_data)
        session.add(new_chat)
        session.commit()
        session.refresh(new_chat)
        return new_chat

    def chat_exists(self, name: str, session: Session) -> bool:
        user = self.get_chat_by_name(chat_name=name, session=session)
        if user:
            return True
        return False

    def get_chat_by_name(self, chat_name: str, session: Session) -> Optional[Chat]:
        statement = select(Chat).where(Chat.name == chat_name)
        result = session.exec(statement).first()
        return result

    def get_all_chats(self, session: Session) -> Any:
        statement = select(Chat)
        result = session.exec(statement).all()
        return result

    def get_all_chats_user(self, session: Session, user_id: str) -> Any:
        statement = select(Chat).where(Chat.user_id == uuid.UUID(user_id))
        result = session.exec(statement).all()
        return result

    def update_chat(self):
        pass

    def delete_chat(self):
        pass
