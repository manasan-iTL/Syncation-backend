from email.policy import default
from operator import index
from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
import uuid
from sqlalchemy_utils import UUIDType

from api.db import Base


class Room(Base):
    __tablename__ = "room"
    
    id = Column(UUIDType(binary=False), default=uuid.uuid4, unique=True, primary_key=True)
    host_id = Column(UUIDType(binary=False))
    title = Column(String(1024), default="しんけーしょん るーむ1")
    timer = Column(String(1024))
    milisecond = Column(String(1024), default="00")
    num = Column(Integer, default=0)
    mode = Column(String(1024), default="chat_always")
    user = relationship("User", back_populates="room", uselist=False)
    vote = relationship("Vote", back_populates="room", uselist=False)

class User(Base):
    __tablename__ = "user"
    id = Column(UUIDType(binary=False), default=uuid.uuid4, unique=True, primary_key=True)
    username = Column(String(1024), default="Guest")
    status = Column(String(1024), default="player")
    room_id = Column(UUIDType(binary=False), ForeignKey("room.id"), nullable=True)
    is_host = Column(Boolean, default=False)
    room = relationship("Room", back_populates="user", uselist=False)
 
class Vote(Base):
    __tablename__ = "vote"
    id = Column(Integer, primary_key=True)
    time = Column(String(1024))
    rest_flag = Column(Boolean, default=False)
    room_id = Column(UUIDType(binary=False), ForeignKey("room.id"), nullable=True)
    turn = Column(Integer)
    room = relationship("Room", back_populates="vote", uselist=False)

