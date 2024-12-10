from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi import Request
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.api.auth.utils import decode_token
from src.api.auth.utils import token_in_blacklist
from src.api.db.main import get_session
from src.api.db.models.user import User
from src.api.resources.user_manager import UserManager

from typing import Optional
from typing import Dict
from typing import Any
from typing import List


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)
        token = creds.credentials
        if token and not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )

        token_data = decode_token(token)
        if token_in_blacklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token has been revoked"
            )

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        if token_data:
            return True
        return False

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Method not implemented")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
            )


def get_current_user(
    token_details: Dict[str, Any] = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
) -> User:
    user_email = token_details["user"]["email"]
    user = UserManager().get_user_by_email(email=user_email, session=session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return True
