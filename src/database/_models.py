from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column, 
    DateTime, 
    String, 
    Integer,
) 


class Base(DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = "test_profiles"
    
    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, default=datetime.utcnow)
    full_name = Column(String)
