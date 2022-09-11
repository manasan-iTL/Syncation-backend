from email.policy import default
from operator import index
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from api.db import Base


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer)
    title = Column(String(1024))
    timer = Column(String(1024))
    mode = Column(String(1024))
    user = relationship("User", back_populates="room", uselist=False)
    

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    username = Column(String(1024))
    status = Column(String(1024))
    room_id = Column(Integer, ForeignKey("room.id"), nullable=True, default=None)
    room = relationship("Room", back_populates="user", uselist=False)


