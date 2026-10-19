from sqlalchemy import Column, BigInteger, String, Integer, DateTime, text
from app.db.database import Base


class CampusInfo(Base):
    __tablename__ = "campus_info"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    school_name = Column(String(100), nullable=False)
    college_name = Column(String(100))
    class_name = Column(String(100))
    level = Column(Integer, nullable=False)
    parent_id = Column(BigInteger)
    sort = Column(Integer, default=0)
    status = Column(Integer, default=1)
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
