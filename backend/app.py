from contextlib import asynccontextmanager
from db import init_db
from fastapi import FastAPI
from src.routes.user import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield 



app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
