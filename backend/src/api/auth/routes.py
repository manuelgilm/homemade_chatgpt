from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session
from src.db.main import get_session
from src.auth.schemas import UserCreateModel
from src.auth.schemas import UserModel
from src.resources.user_manager import UserManager

user_router = APIRouter()


# create
@user_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: UserCreateModel,
    session: Session = Depends(get_session),
    manager: UserManager = Depends(UserManager),
):
    user_email = user_data.email
    user_exists = manager.user_exists(email=user_email, session=session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists",
        )

    new_user = manager.create_user(session=session, user_data=user_data)
    return new_user.model_dump()


# read
@user_router.get("/user/{user_id}")
async def read_user(user_id: int, manager: UserManager = Depends(UserManager)):
    return {"message": "User read"}


# update
@user_router.put("/user/{user_id}")
async def update_user(user_id: int):
    return {"message": "User updated"}


# delete
@user_router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    return {"message": "User deleted"}
