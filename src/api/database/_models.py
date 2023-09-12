from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import (
    Table,
    Column, 
    ForeignKey,
    DateTime, 
    String, 
    Integer,
) 


class Base(DeclarativeBase):
    pass


questions_asked_table = Table(
    "questions_asked",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("question_id", ForeignKey("questions.id"), primary_key=True),
)


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True)
    users_asked = relationship(
        "User", 
        secondary=questions_asked_table, 
        back_populates="questions_asked",
    )
    
    creation_date = Column(DateTime, default=datetime.utcnow)
    text = Column(String, unique=True)
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    questions_asked = relationship(
        "Question", 
        secondary=questions_asked_table, 
        back_populates="users_asked",
    )
    
    creation_date = Column(DateTime, default=datetime.utcnow)
    email = Column(String, unique=True, index=True)

