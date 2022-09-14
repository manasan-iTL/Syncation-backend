from api.models.room import Room
from pydantic import BaseModel

class RoomRequest(BaseModel):
    host_id: str
    timer: str
    milisecond: str
    num: int
    title: str
    mode: str
    class Config():
        orm_mode = True
    # room作成時idは不要
        
class Room(RoomRequest):
    id: str 
    class Config():
        orm_mode = True

class UserRequest(BaseModel):
    username: str
    status: str
    room_id: str
    is_host : bool
    class Config():
        orm_mode = True

class User(BaseModel):
    id: str
    username: str
    status: str
    room_id: str
    is_host : bool
    class Config():
        orm_mode = True
        
class TodoBase(BaseModel):
    name: str
    checked: str
    user_id: str
    class Config():
        orm_mode = True

class ProgressBase(BaseModel):
    percent: int
    user_id: str
    class Config():
        orm_mode = True

class VoteBase(BaseModel):
    id: str
    time: str
    room_id: str
    class Config():
        orm_mode = True

class RestBase(BaseModel):
    time: str
    res_flag: str
