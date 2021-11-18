from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from .database import Base

class Task(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    task = Column(String)

