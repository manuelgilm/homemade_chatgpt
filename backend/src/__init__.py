from fastapi import FastAPI
from src.auth.routes import user_router
from src.settings.db import init_db
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
    lifespan=lifespan
)

app.include_router(user_router, prefix=f"/api/{version}/users")

