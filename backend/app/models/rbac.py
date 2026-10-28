from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
    text,
)

from app.db.database import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    status = Column(Integer, nullable=False, server_default=text("1"))
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Permission(Base):
    __tablename__ = "permission"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(80), nullable=False, unique=True)
    name = Column(String(80), nullable=False)
    resource = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    description = Column(String(255))
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class UserRole(Base):
    __tablename__ = "user_role"
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", "club_id", name="uk_user_role_scope"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    role_id = Column(BigInteger, nullable=False, index=True)
    club_id = Column(BigInteger, nullable=False, server_default=text("0"))
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class RolePermission(Base):
    __tablename__ = "role_permission"
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uk_role_permission"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(BigInteger, nullable=False, index=True)
    permission_id = Column(BigInteger, nullable=False, index=True)
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
