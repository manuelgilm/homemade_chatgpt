from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session
from src.api.resources.user_manager import UserManager
from src.api.auth.schemas import UserCreateModel
from src.api.auth.schemas import UserModel
from src.api.auth.schemas import UserLoginModel
from src.api.auth.dependencies import AccessTokenBearer
from src.api.auth.dependencies import RefreshTokenBearer
from src.api.auth.dependencies import RoleChecker
from src.api.auth.dependencies import get_current_user
from src.api.auth.utils import create_access_token
from src.api.auth.utils import verify_passwd
from src.api.db.main import get_session
from src.api.auth.utils import add_jti_to_blocklist
from src.api.settings.configs import REFRESH_TOKEN_EXPIRY
from datetime import timedelta
from datetime import datetime

from fastapi.responses import JSONResponse

auth_router = APIRouter(tags=["auth"])
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin"])


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


@auth_router.post("/refresh_token")
async def get_new_access_token(
    token_details: RefreshTokenBearer = Depends(RefreshTokenBearer()),
):

    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": token})

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
    )


@auth_router.get("/logout")
async def revoke_token(token_details: AccessTokenBearer = Depends(access_token_bearer)):
    jti = token_details["jti"]

    add_jti_to_blocklist(jti)
    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )


@auth_router.get("/me")
async def get_current_user(user_details=Depends(get_current_user)):
    return user_details


@auth_router.post("/create_admin")
async def create_admin(
    session: Session = Depends(get_session),
    manager: UserManager = Depends(UserManager),
):
    user_data = UserCreateModel(
        email="admin@admin.com",
        last_name="admin",
        first_name="admin",
        username="admin",
        password="admin123",
    )

    user_email = user_data.email
    user_exists = manager.user_exists(email=user_email, session=session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists",
        )

    new_user = manager.create_user(session=session, user_data=user_data, role="admin")
    return new_user.model_dump()


# admin operations
@auth_router.get("/users/all", dependencies=[Depends(role_checker)])
async def list_users(
    session: Session = Depends(get_session),
    manager: UserManager = Depends(UserManager),
    role_checker: RoleChecker = Depends(role_checker),
):
    users = manager.list_users(session=session)

    return users
