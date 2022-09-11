

import api.schemas.room as room_schema
import api.models.room as room_model
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result

async def create_user(db: AsyncSession, request: room_schema.UserRequest):
    new_user = room_model.User(
        username = request.username,
        status = request.status,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user.id

async def get_user(db: AsyncSession, id: str):
    q = select(
        room_model.User.id,
        room_model.User.username,
        room_model.User.status,
        room_model.User.room_id,
    ).filter(room_model.User.id == id )
    result = await db.execute(q)
    return result.first()