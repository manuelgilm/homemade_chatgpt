from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session
from src.api.db.main import get_session
from src.api.auth.schemas import UserCreateModel
from src.api.auth.schemas import UserModel
from src.api.auth.schemas import UserLoginModel
from src.api.resources.user_manager import UserManager
from src.api.auth.dependencies import AccessTokenBearer
from datetime import timedelta

from src.api.auth.utils import create_access_token
from src.api.auth.utils import verify_passwd
from fastapi.responses import JSONResponse
from src.api.settings.configs import REFRESH_TOKEN_EXPIRY

auth_router = APIRouter(tags=["auth"])
access_token_bearer = AccessTokenBearer()


# create
@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
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


# login
@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel,
    session: Session = Depends(get_session),
    manager: UserManager = Depends(UserManager),
):
    user = manager.get_user_by_email(email=login_data.email, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not verify_passwd(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.id)}
    )

    refresh_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.id)},
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
    )
    return JSONResponse(
        content={
            "message": "Login Successful",
            "access_token": token,
            "refresh_token": refresh_token,
            "user": {"email": user.email, "uid": str(user.id)},
        }
    )


# read
@auth_router.get("/user/{user_id}")
async def read_user(user_id: int, manager: UserManager = Depends(UserManager)):
    return {"message": "User read"}


# update
@auth_router.put("/user/{user_id}")
async def update_user(user_id: int):
    return {"message": "User updated"}


# delete
@auth_router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    return {"message": "User deleted"}


@auth_router.get("/protected")
async def protected_route(user_details=Depends(access_token_bearer)):
    print(user_details)
    return {"message": "Protected route"}
