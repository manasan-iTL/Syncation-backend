from email.policy import default
from operator import index
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
import uuid
from sqlalchemy_utils import UUIDType

from api.db import Base


class Room(Base):
    __tablename__ = "room"
    
    id = Column(UUIDType(binary=False), default=uuid.uuid4, unique=True, primary_key=True)
    host_id = Column(UUIDType(binary=False))
    title = Column(String(1024))
    timer = Column(String(1024))
    mode = Column(String(1024))
    user = relationship("User", back_populates="room", uselist=False)
    

class User(Base):
    __tablename__ = "user"
    id = Column(UUIDType(binary=False), default=uuid.uuid4, unique=True, primary_key=True)
    username = Column(String(1024))
    status = Column(String(1024))
    room_id = Column(UUIDType(binary=False), ForeignKey("room.id"), nullable=True)
    room = relationship("Room", back_populates="user", uselist=False)
    @property
    def attr(self):
        return self._attr


