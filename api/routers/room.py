from contextlib import nullcontext
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.room as room_schemas 
import api.cruds.room as room_crud
import api.models.room as room_model
from api.db import get_db
from typing import List
import random

router = APIRouter()

@router.post("/host")
async def create_host(request_user: room_schemas.UserRequest, request_room: room_schemas.RoomRequest, db: AsyncSession = Depends(get_db)):
    user_id = await room_crud.create_user(db, request=request_user)
    request_room.host_id = user_id
    request_room.num = 1 # ホスト分の人数を追加
    room_id = await room_crud.create_room(db, request=request_room)
    request_user.room_id = room_id
    request_user.is_host = True # host権限付与用フラグ
    user = await update_user(db=db, user_id=user_id, user_body=request_user)
    return {"user_id": user_id, "room_id": room_id}
    # redirectはフロントで行う？

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
    user = await room_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await room_crud.update_user(db, request=user_body, original=user)

@router.delete("/user/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await room_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await room_crud.delete_user(db, original=user)




@router.get("/rooms")
async def list_room(db: AsyncSession = Depends(get_db)):
    return await room_crud.list_room(db)

@router.post("/room")
async def create_room(request: room_schemas.RoomRequest, db: AsyncSession = Depends(get_db)):
    return await room_crud.create_room(db, request)

@router.put("/room/{room_id}")
async def update_room(room_id: str, room_body: room_schemas.RoomRequest, db: AsyncSession = Depends(get_db)):
    room = await room_crud.get_room(db, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await room_crud.update_room(db, request=room_body, original=room)

@router.delete("/room/{room_id}")
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    room = await room_crud.get_room(db, room_id=room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    return await room_crud.delete_room(db, original=room)

@router.get("/room/{room_id}")
async def get_room(room_id: str, db: AsyncSession = Depends(get_db)):
    return await room_crud.get_room(db, room_id)

@router.get("/room/{room_id}/users")
async def get_room(room_id: str, db: AsyncSession = Depends(get_db)):
    room = await room_crud.get_room(db, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return await room_crud.get_room_users_and_num(db, room_original=room)

@router.post("/enter/{room_id}/{user_id}")
async def enter_room(room_id: str, user_id: str, db: AsyncSession = Depends(get_db)):
    user = await room_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    room = await room_crud.get_room(db, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    if user.room_id:
        raise HTTPException(status_code=400, detail="Already in the room")
    return await room_crud.enter_room(db, room_original=room, user_original=user)

@router.post("/leave/{room_id}/{user_id}")
async def leave_room(room_id: str, user_id: str, db: AsyncSession = Depends(get_db)):
    user = await room_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    room = await room_crud.get_room(db, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    if user.room_id is None:
        raise HTTPException(status_code=400, detail="Not in the room")
    elif user.room_id != room.id:
        raise HTTPException(status_code=400, detail="Diffrent room")
    return await room_crud.leave_room(db, room_original=room, user_original=user)

@router.post("/room/{room_id}/vote/{turn}")
async def register_vote(room_id: str, turn: int,  request: room_schemas.VoteRequest, db: AsyncSession = Depends(get_db)):
    if request.rest_flag is False:
        request.time = str(0)   
    request.room_id = room_id
    request.turn = turn
    return await room_crud.register_vote(db, request)

@router.get("/room/{room_id}/vote/{turn}")
async def vote_result(room_id: str, turn: int, db: AsyncSession = Depends(get_db)):
    vote_list = await room_crud.get_vote_by_turn(db, room_id, turn)
    vote_time_list = [vote[0].time for vote in vote_list]
    res_time = random.choice(vote_time_list)
    print(vote_time_list)
    return {"res_time": res_time, "vote_time_list": vote_time_list}    
