from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, primary_key=True)
    timer = Column(String(1024))
    title = Column(String(1024))
    mode = Column(String(1024))

    # done = relationship("Done", back_populates="task")