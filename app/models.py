from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class LineManager(Base):
    __tablename__ = "line_manager"

    id = Column(Integer, primary_key=True, index=True)
    user_id = relationship("User", back_populates="line_manager")
