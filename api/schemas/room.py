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
    progress: int
    class Config():
        orm_mode = True

class User(UserRequest):
    id: str
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

class VoteRequest(BaseModel):
    time: str
    room_id: str
    rest_flag: bool
    turn: int
    class Config():
        orm_mode = True

