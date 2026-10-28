from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    Integer,
    DateTime,
    text,
)
from app.db.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False)
    real_name = Column(String(50))
    student_no = Column(String(30))
    gender = Column(Integer)
    phone = Column(String(20))
    email = Column(String(100))
    school_name = Column(String(100))
    college_name = Column(String(100))
    class_name = Column(String(100))
    complete_time = Column(DateTime)
    avatar_url = Column(String(255))
    token = Column(String(255))
    token_version = Column(Integer, nullable=False, server_default=text("0"))
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
