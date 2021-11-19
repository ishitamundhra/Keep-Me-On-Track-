from sqlalchemy import Column, Integer, String
from database import Base

class Task(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    task = Column(String)
    status = Column(String)
