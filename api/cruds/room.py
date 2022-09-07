from sqlalchemy.orm.session import Session
import api.schemas.room as room_schema
import api.models.room as room_model
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy.engine import Result

async def create_user(db: Session, request: room_schema.UserBase):
    new_user = room_model.User(
        username = request.username,
        status = request.status,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user.id

async def get_user(db: AsyncSession, id: int):
    return db.query(room_model.User).filter(room_model.User.id == id).first()


async def create_room(db: AsyncSession, request: room_schema.RoomBase):
    new_room = room_model.Room(
        host_id = request.host_id,
        timer = request.timer,
        title = request.title,
        mode = request.mode,
    )
    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)
    return new_room.id


async def update_room(db: Session, room_id: str, request: room_schema.Room):
    result: Result = db.query(room_model.Room).filter(room_model.Room.id == room_id).first()  
    result.timer = request.timer,
    result.title = request.title,
    result.mode = request.mode,
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


async def enter_room(db: AsyncSession, room_id: str, user_id: str):
    result: Result = db.query(room_model.User).filter(room_model.User.id == user_id).first()  
    result.room_id = room_id
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return 'success'

async def delete_room(db: AsyncSession, room_id: str):
    result: Result = db.query(room_model.User).filter(room_model.User.id == room_id).first()  
    result.room_id = room_id
    await db.delete(result)
    await db.commit()

async def vote(db: AsyncSession, room_id: str, request: room_schema.RestBase):
    result: Result = db.query(room_model.User).filter(room_model.User.id == room_id).first()  
    