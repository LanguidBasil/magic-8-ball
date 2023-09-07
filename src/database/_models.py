from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column, 
    ForeignKey,
    DateTime, 
    String, 
    Integer,
) 


class Base(DeclarativeBase):
    pass


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True)
    
    creation_date = Column(DateTime, default=datetime.utcnow)
    text = Column(String, unique=True)
    total_voices = Column(Integer, default=0)
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    questions = Column(ForeignKey(Question.id))
    
    creation_date = Column(DateTime, default=datetime.utcnow)
    email = Column(String, unique=True)

