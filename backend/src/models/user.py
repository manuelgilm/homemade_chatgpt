from sqlmodel import SQLModel
from sqlmodel import Field 
from sqlalchemy import Column
from sqlalchemy import String

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, max_length=50)
    email: str = Field(sa_column=Column("email", String, unique=True, index=True))
    hashed_password: str = Field(max_length=50)





