from pydantic import BaseModel
from pydantic import Field
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=50)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "user",
                "last_name": "user",
                "username": "user",
                "email": "user@user.com",
                "password": "user123",
            }
        }
    }


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserLoginModel(BaseModel):
    email: str
    password: str
