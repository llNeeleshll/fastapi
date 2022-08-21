from email.policy import default
from enum import unique
from operator import index
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique=True, index = True)
    user_name = Column(String, unique=True, index = True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    all_todos = relationship("Todo", back_populates="created_by_user")

class Todo(Base):

    __tablename__ = "todo"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    created_by_user = relationship("User", back_populates="all_todos")
