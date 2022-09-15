import api.schemas.room as room_schemas
import api.models.room as room_model
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional
from fastapi import FastAPI, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.engine import Result

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
    original.username = request.username
    original.status = request.status
    original.is_host = request.is_host
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_user(db: AsyncSession, original: room_model.User):
    await db.delete(original)
    await db.commit()


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

async def update_room(
    db: AsyncSession, request: room_schemas.RoomRequest, original: room_model.Room) -> room_model.Room:
    print(original)
    original.host_id = request.host_id
    original.title = request.title
    original.timer = request.timer
    original.num = request.num
    original.mode = request.mode
    original.milisecond = request.milisecond
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_room(db: AsyncSession, original: room_model.Room):
    await db.delete(original)
    await db.commit()

async def enter_room(db: AsyncSession, room_original: room_model.Room, user_original: room_model.User):

    user_original.room_id = room_original.id
    room_original.num += 1
    db.add(room_original)
    db.add(user_original)
    await db.commit()
    await db.refresh(room_original)
    await db.refresh(user_original)
    obj = await get_room_users_and_num(db, room_original)
    return {"message": "succes", "num": obj["num"], "users": obj["users"]}
    # 部屋にいるuserの数、一覧を返す

async def leave_room(db: AsyncSession, room_original: room_model.Room, user_original: room_model.User):

    user_original.room_id = None
    room_original.num -= 1
    db.add(room_original)
    db.add(user_original)
    await db.commit()
    await db.refresh(room_original)
    await db.refresh(user_original)
    obj = await get_room_users_and_num(db, room_original)
    return {"message": "succes", "num": obj["num"], "users": obj["users"]}

async def get_room_users_and_num(db: AsyncSession, room_original: room_model.Room):
    q_user = select(room_model.User).filter(room_model.User.room_id==room_original.id)
    result_user = await db.execute(q_user)
    users = result_user.all()

    q_room = select(room_model.Room).filter(room_model.Room.id==room_original.id)
    result_room = await db.execute(q_room)
    room = result_room.first()
    num = room[0].num
    return {"num": num, "users": users}

async def register_vote(db: AsyncSession, request: room_schemas.VoteRequest):
    new_vote = room_model.Vote(
        room_id = request.room_id,
        time = request.time,
        turn = request.turn,
        rest_flag = request.rest_flag,
    )
    db.add(new_vote)
    await db.commit()
    await db.refresh(new_vote)
    return new_vote

async def get_vote_by_turn(db: AsyncSession, room_id: str, turn: int):
    q = select(room_model.Vote).filter(room_model.Vote.room_id == room_id, room_model.Vote.turn == turn)
    result = await db.execute(q)
    votes = result.all()
    print(votes)
    return votes if votes is not None else None