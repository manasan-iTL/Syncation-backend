from typing import Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")
    # user_id: Optional[str] = Field(None, example="abcde123")

class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")
    user_id: Optional[str] = Field(None, example="abcde123")
    
    class Config:
        orm_mode = True