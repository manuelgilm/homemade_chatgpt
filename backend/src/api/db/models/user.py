import uuid
from sqlmodel import SQLModel
from sqlmodel import Field
from sqlalchemy import Column
from sqlalchemy import String
from datetime import datetime


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True)
    username: str = Field(index=True, max_length=50)
    email: str = Field(sa_column=Column("email", String, unique=True, index=True))
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    is_verified: bool = Field(default=False)
    hashed_password: str = Field(max_length=50)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    def __repr__(self):
        return f"<User {self.username}>"
