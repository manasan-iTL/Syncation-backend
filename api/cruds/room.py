import api.schemas.room as room_schemas
import api.models.room as room_model
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional
from fastapi import FastAPI, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.engine import Result
from copy import deepcopy

async def create_user(db: AsyncSession, request: room_schemas.UserRequest):
    new_user = room_model.User(
        username = request.username,
        status = request.status,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user.id

async def get_user(db: AsyncSession, user_id: str):
    q = select(
        room_model.User,
    ).filter(room_model.User.id == user_id )
    result = await db.execute(q)
    user = result.first()
    return user[0] if user is not None else None

async def list_user(db: AsyncSession) -> List[room_schemas.User]:
    q = select(room_model.User)
    print(q)
    result = await db.execute(q)
    users = result.all()
    return users

async def update_user(
    db: AsyncSession, request: room_schemas.UserRequest, original: room_model.User) -> room_model.User:
    original.room_id = request.room_id
    print(original)
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def create_room(db: AsyncSession, request: room_schemas.RoomRequest):
    new_room = room_model.Room(
        host_id = request.host_id,
        title = request.title,
        timer = request.timer,
        mode = request.mode,
    )
    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)
    return new_room.id

async def get_room(db: AsyncSession, id: str):
    q = select(
        room_model.Room.id,
        room_model.Room.host_id,
        room_model.Room.title,
        room_model.Room.timer,
        room_model.Room.mode,
    ).filter(room_model.Room.id == id )
    result = await db.execute(q)
    return result.first()
