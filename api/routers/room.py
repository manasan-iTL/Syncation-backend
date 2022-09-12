from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.room as room_schemas 
import api.cruds.room as room_crud
import api.models.room as room_model
from api.db import get_db
from typing import List


router = APIRouter()

@router.post("/host")
async def create_host(request_user: room_schemas.UserRequest, request_room: room_schemas.RoomRequest, db: AsyncSession = Depends(get_db)):
    user_id = await room_crud.create_user(db, request_user)
    request_room.host_id = user_id
    room_id = await room_crud.create_room(db, request_room)
    return {"user_id": user_id, "room_id": room_id}

@router.get("/users")
async def list_user(db: AsyncSession = Depends(get_db)):
    return await room_crud.list_user(db)

@router.post("/user")
async def create_user(request: room_schemas.UserRequest, db: AsyncSession = Depends(get_db)):
    return await room_crud.create_user(db, request)

@router.get("/user/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    return await room_crud.get_user(db, user_id)

@router.put("/user/{user_id}")
async def update_user(user_id: str, user_body: room_schemas.UserRequest, db: AsyncSession = Depends(get_db)):
    user = await room_crud.get_user(db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await room_crud.update_user(db, request=user_body, original=user)

@router.post("/room")
async def create_room(request: room_schemas.RoomRequest, db: AsyncSession = Depends(get_db)):
    return await room_crud.create_room(db, request)

@router.get("/room/{room_id}")
async def get_room(room_id: str, db: AsyncSession = Depends(get_db)):
    return await room_crud.get_room(db, room_id)