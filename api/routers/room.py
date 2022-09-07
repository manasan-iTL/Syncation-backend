from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.room as room_schemas 
import api.cruds.room as room_crud
from api.db import get_db

router = APIRouter()

@router.post("/create")
async def create_room(request: room_schemas.RoomBase, db: AsyncSession = Depends(get_db)):
    return room_crud.create_room(db, request)

@router.post("/update/{room_id}")
async def udate_room(room_id: str, request: room_schemas.Room,  db: AsyncSession = Depends(get_db)):
    return room_crud.update_room(db, room_id, request)

@router.post("/enter/{room_id}")
async def enter_room(db: AsyncSession, room_id: str, user_id: str):
    return room_crud.enter_room(db, room_id, user_id)


@router.delete("/room/{room_id}")
async def delete_room(room_id: str, db: AsyncSession = Depends(get_db)):
    return room_crud.delete_room(db, room_id)


@router.post("/roome/vote/{room_id}")
async def vote(db: AsyncSession, room_id: str, request: room_schemas.RestBase):
    return room_crud.vote(db, room_id, request)

