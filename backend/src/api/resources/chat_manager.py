from fastapi import Depends
from sqlmodel import Session
from typing import Dict
from typing import Any
from src.api.db.models.chat import Chat

# from src.api.db.models.chat import ChatSession
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

    def delete_chat_by_name(self, session: Session, chat_name: str) -> bool:
        statement = select(Chat).where(Chat.name == chat_name)
        result = session.exec(statement).first()
        session.delete(result)
        session.commit()
        return {"detail": "Chat deleted"}

    def delete_chat(self, session: Session, chat_id: str) -> bool:
        statement = select(Chat).where(Chat.id == uuid.UUID(chat_id))
        result = session.exec(statement).first()
        if result:
            session.delete(result)
            session.commit()
            return {"detail": "Chat deleted"}
        return {"detail": "Chat not found"}


# class ChatSessionManager:

#     def __init__(self):
#         pass

#     def create_chat_session(self, session: Session, user_id: str, chat_id: str) -> Any:
#         new_chat_session = ChatSession(
#             user_id=uuid.UUID(user_id), chat_id=uuid.UUID(chat_id), chat_history=[]
#         )

#     def chat_history(self):
#         pass

#     def get_user_messages(session_id: str):
#         """
#         Returns a dictionary of messages sent by the user
#         structure:
#         user_messages = {
#             "session_id":[{
#                 "message":"some text",
#                 "created_at":"date time",
#                 "reactions":[]
#                 }]
#         }
#         """
#         pass

#     def get_user_interactions(session_id: str):
#         """
#         Returns a dictionary of interactions with the user.
#         Defining interaction as a collection of messages sent by the user with
#         the answers from the chatbot.

#         structure:
#         user_interactions = {
#             "session_id":[{
#                 "message":"some text",
#                 "created_at":"date time",
#                 "reactions":[]
#                 }]
#         }

#         """
#         pass
