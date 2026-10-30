from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    Text,
    DateTime,
    Index,
    UniqueConstraint,
    text,
)
from app.db.database import Base


class Club(Base):
    __tablename__ = "club"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    icon_url = Column(String(255))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Integer, default=1)
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class ClubMember(Base):
    __tablename__ = "club_member"
    __table_args__ = (
        UniqueConstraint("club_id", "user_id", name="uk_club_user"),
        Index("idx_user_status", "user_id", "status"),
        Index("idx_club_status", "club_id", "status"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    club_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    status = Column(Integer, nullable=False, default=0)
    apply_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    join_time = Column(DateTime)
    audit_user_id = Column(BigInteger)
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
