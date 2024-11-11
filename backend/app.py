from contextlib import asynccontextmanager
from sqlmodel import create_engine
from sqlmodel import SQLModel
from sqlmodel import Session

from fastapi import FastAPI



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)    

engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables(engine=engine)
    yield 
    SQLModel.metadata.drop_all(engine)



from src.routes.user import user_router
app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
