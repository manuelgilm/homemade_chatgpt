from fastapi import FastAPI
from src.api.auth.routes import auth_router
from src.api.chat.routes import chat_router
from src.api.db.main import init_db
from contextlib import asynccontextmanager

from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


middleware = [Middleware(SessionMiddleware, secret_key="", https_only=True)]

version = "v1"
app = FastAPI(
    title="FastAPI with async context manager",
    version=version,
    description="This is a FastAPI app with async context manager",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix=f"/api/{version}/auth")
# app.include_router(chat_router, prefix=f"/api/{version}/chat")
