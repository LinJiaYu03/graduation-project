from sqlalchemy import Column, BigInteger, String, Boolean, Integer, Text, Numeric, DateTime, text
from app.db.database import Base


class Activity(Base):
    __tablename__ = "activity"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    image_urls = Column(Text)
    name = Column(String(200), nullable=False)
    club_id = Column(BigInteger, nullable=False)
    description = Column(Text)
    location = Column(String(200))
    notice = Column(Text)
    registration_start_time = Column(DateTime)
    registration_end_time = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    max_participants = Column(Integer)
    current_participants = Column(Integer, default=0)
    need_audit = Column(Boolean, default=False)
    activity_type = Column(String(50))
    activity_level = Column(String(50))
    status = Column(String(20), default="审核中")
    audit_status = Column(Integer, default=0)
    audit_time = Column(DateTime)
    audit_user_id = Column(BigInteger)
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    score = Column(String(255), default="0")
    is_published = Column(Boolean, default=True)


class ActivityRegistration(Base):
    __tablename__ = "activity_registration"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    activity_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    status = Column(String(20), default="待审核")
    score = Column(Numeric(5, 2))
    comment = Column(Text)
    audit_user_id = Column(BigInteger)
    audit_time = Column(DateTime)
    registration_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class ActivityCheckin(Base):
    __tablename__ = "activity_checkin"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    activity_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    checkin_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
