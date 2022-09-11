from api.routers import task, done
import os
from fastapi import FastAPI, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Column, TIMESTAMP, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import FetchedValue

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)


class Room(Base):
    __tablename__ = "room"
    id = Column(String(1024), primary_key=True, index=True)
    host_id = Column(String(1024), ForeignKey("user.id"))
    title = Column(String(1024))
    timer = Column(String(1024))
    mode = Column(String(1024))

class User(Base):
    __tablename__ = "user"
    id = Column(String(1024), primary_key=True, index=True)
    username = Column(String(1024))
    status = Column(String(1024))
    room_id = Column(String(1024), ForeignKey("room.id"))



