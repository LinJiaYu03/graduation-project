from sqlalchemy import Column,Integer,String,DateTime
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(255))
    password=Column(String(255))
    age=Column(Integer)
    create_time=Column(DateTime, default=datetime.now())
    update_time=Column(DateTime, default=datetime.now(), onupdate=datetime.now())
