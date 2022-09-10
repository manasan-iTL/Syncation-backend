from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(1024))
    status = Column(String(1024))
    room_id = Column(String(1024))

    # done = relationship("Done", back_populates="task")