from sqlalchemy import Column, BigInteger, String, Boolean, Integer, Text, DateTime, text
from app.db.database import Base


class Club(Base):
    __tablename__ = "club"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    icon_url = Column(String(255))
    name = Column(String(100), nullable=False)
    tags = Column(String(255))
    description = Column(Text)
    status = Column(Integer, default=1)
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    level_tag = Column(String(255))


class ClubMember(Base):
    __tablename__ = "club_member"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    club_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    is_manager = Column(Boolean, default=False)
    join_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
