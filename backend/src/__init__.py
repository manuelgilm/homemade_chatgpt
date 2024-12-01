from fastapi import FastAPI
from src.api.auth.routes import auth_router
from src.api.chat.routes import chat_router
from src.api.db.main import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


version = "v1"
app = FastAPI(
    title="FastAPI with async context manager",
    version=version,
    description="This is a FastAPI app with async context manager",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix=f"/api/{version}/auth")
app.include_router(chat_router, prefix=f"/api/{version}/chat")
