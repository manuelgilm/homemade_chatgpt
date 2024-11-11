from fastapi import APIRouter 
from sqlmodel import Session
from fastapi import Depends
from app import get_session
from src.models.user import User
from sqlmodel import select

user_router = APIRouter(prefix="/users")


@user_router.get("/user/{username}")
async def create_user(username:str, session: Session = Depends(get_session)):    
    user = session.exec(select(User).where(User.username == username)).one()
    if not user:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.model_dump()
    return {"error": "User already exists"}


@user_router.get("/user/{username}")
async def get_user(username:str, session: Session=Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).one()
    if not user:
        return {"error": "User not found"}
    return user.model_dump()


@user_router.put("/user/{username}")
async def update_user(username:str, user: User, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).one()
    if not user:
        return {"error": "User not found"}
    user.username = user.username
    user.email = user.email
    session.add(user)
    session.commit()
    session.refresh(user)
    return user.model_dump()


@user_router.delete("/user/{username}")
async def delete_user(username:str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).one()
    if not user:
        return {"error": "User not found"}
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}


@user_router.get("/users")
async def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return [user.model_dump() for user in users] 