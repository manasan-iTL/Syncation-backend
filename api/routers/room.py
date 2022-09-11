from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.room as room_schemas 
import api.cruds.room as room_crud
from api.db import get_db


router = APIRouter()

@router.post("/user")
async def create_user(request: room_schemas.UserBase, db: AsyncSession = Depends(get_db)):
    return await room_crud.create_user(db, request)

@router.get("/user/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    return await room_crud.get_user(db, user_id)