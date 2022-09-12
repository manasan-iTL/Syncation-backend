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
        is_host = request.is_host,
    )
    print(new_user.is_host)
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
    result = await db.execute(q)
    users = result.all()
    return users

async def update_user(
    db: AsyncSession, request: room_schemas.UserRequest, original: room_model.User) -> room_model.User:
    original.room_id = request.room_id
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
        num = request.num,
    )
    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)
    return new_room.id

async def get_room(db: AsyncSession, room_id: str):
    q = select(room_model.Room).filter(room_model.Room.id == room_id )
    result = await db.execute(q)
    room = result.first()
    return room[0] if room is not None else None

async def list_room(db: AsyncSession) -> List[room_schemas.Room]:
    q = select(room_model.Room)
    result = await db.execute(q)
    rooms = result.all()
    return rooms

async def enter_room(db: AsyncSession, room_original: room_model.Room, user_original: room_model.User):

    user_original.room_id = room_original.id
    room_original.num += 1
    db.add(room_original)
    db.add(user_original)
    await db.commit()
    await db.refresh(room_original)
    await db.refresh(user_original)
    obj = await get_room_users_and_num(db, room_original, user_original)
    return {"message": "succes", "num": obj["num"], "users": obj["users"]}
    # 部屋にいるuserの数、一覧を返す

async def get_room_users_and_num(db: AsyncSession, room_original: room_model.Room, user_original: room_model.User):
    q_user = select(room_model.User).filter(room_model.User.room_id==room_original.id)
    print("q_user", q_user)
    result_user = await db.execute(q_user)
    print("result_user", result_user)
    users = result_user.all()
    print("users", users)

    q_room = select(room_model.Room).filter(room_model.Room.id==room_original.id)
    result_room = await db.execute(q_room)
    room = result_room.first()
    num = room[0].num
    return {"num": num, "users": users}