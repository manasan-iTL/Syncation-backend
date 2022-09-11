

import api.schemas.room as room_schema
import api.models.room as room_model
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy.engine import Result

async def create_user(db: AsyncSession, request: room_schema.UserBase):
    new_user = room_model.User(
        username = request.username,
        status = request.status,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user.id

async def get_user(db: AsyncSession, id: str):
    return db.query(room_model.User).filter(room_model.User.id == id).first()