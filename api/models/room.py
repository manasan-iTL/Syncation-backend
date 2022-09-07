from operator import index
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base


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


class Todo(Base):
    __tablename__ = "todo"
    id = Column(String(1024), primary_key=True)
    name = Column(String(1024))
    user_id = Column(String(1024), ForeignKey("user.id"))


class Progress(Base):
    __tablename__ = "progress"
    id = Column(String(1024), primary_key=True)
    percent = Column(Integer)
    user_id = Column(String(1024), ForeignKey("user.id"))

class Vote(Base):
    __tablename__ = "vote"
    id = Column(String(1024), primary_key=True)
    time = Column(String(1024))
    room_id = Column(String(1024), ForeignKey("room.id"))
