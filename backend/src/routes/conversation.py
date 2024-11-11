from src.models.conversation import Conversation
from sqlmodel import Session    
from fastapi import APIRouter
from fastapi import Depends
from app import get_session
from sqlmodel import select

conversation_router = APIRouter(prefix="/conversations")

#Create
@conversation_router.post("/conversation/")
async def create_conversation(conversation:Conversation, session: Session = Depends(get_session)):
    # Validate conversation
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation.model_dump()

#Read
@conversation_router.get("/conversation/{title}")
async def get_conversation(title:str, session: Session = Depends(get_session)):
    conversation = session.exec(select(Conversation).where(Conversation.title == title)).one()
    if not conversation:
        return {"error": "Conversation not found"}
    return conversation.model_dump()

#Update
@conversation_router.put("/conversation/{title}")
async def update_conversation(title:str, conversation: Conversation, session: Session = Depends(get_session)):
    conversation = session.exec(select(Conversation).where(Conversation.title == title)).one()
    if not conversation:
        return {"error": "Conversation not found"}
    conversation.title = conversation.title
    conversation.user_id = conversation.user_id
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation.model_dump()

#Delete
@conversation_router.delete("/conversation/{title}")
async def delete_conversation(title:str, session: Session = Depends(get_session)):
    conversation = session.exec(select(Conversation).where(Conversation.title == title)).one()
    if not conversation:
        return {"error": "Conversation not found"}
    session.delete(conversation)
    session.commit()
    return {"message": "Conversation deleted"}

#List
@conversation_router.get("/conversations")
async def list_conversations(session: Session = Depends(get_session)):
    conversations = session.exec(select(Conversation)).all()
    return [conversation.model_dump() for conversation in conversations]
