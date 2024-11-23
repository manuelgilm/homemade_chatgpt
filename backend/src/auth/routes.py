from fastapi import APIRouter
from src.settings.db import get_session

user_router = APIRouter()

# create 
@user_router.post("/user")
async def create_user():
    return {"message": "User created"}

# read
@user_router.get("/user/{user_id}")
async def read_user(user_id: int):
    return {"message": "User read"}

# update
@user_router.put("/user/{user_id}")
async def update_user(user_id: int):
    return {"message": "User updated"}

# delete
@user_router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    return {"message": "User deleted"}
