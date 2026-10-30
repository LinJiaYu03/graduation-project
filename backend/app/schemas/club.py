from pydantic import BaseModel
from typing import Optional

from app.schemas.user import serialize_user


class ClubRequest(BaseModel):
    iconUrl: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class ClubSearchRequest(BaseModel):
    keyword: Optional[str] = None
    currentPage: Optional[int] = None
    pageSize: Optional[int] = None


class JoinClubRequest(BaseModel):
    clubId: Optional[int] = None


class JoinedClubSearchRequest(BaseModel):
    keyword: Optional[str] = None
    currentPage: Optional[int] = None
    pageSize: Optional[int] = None
    type: Optional[str] = None


class MemberAuditRequest(BaseModel):
    approved: bool = True


class QuitClubRequest(BaseModel):
    clubId: Optional[int] = None


def serialize_club(c, member_count=None) -> dict | None:
    if c is None:
        return None
    return {
        "id": c.id,
        "iconUrl": c.icon_url,
        "name": c.name,
        "description": c.description,
        "status": c.status,
        "createTime": c.create_time,
        "updateTime": c.update_time,
        "memberCount": member_count,
    }


def _user_name(user) -> str | None:
    if user is None:
        return None
    if user.real_name is not None and str(user.real_name).strip() != "":
        return user.real_name
    return user.username


def serialize_club_member(m, user=None, is_manager=False) -> dict | None:
    if m is None:
        return None
    return {
        "id": m.id,
        "clubId": m.club_id,
        "userId": m.user_id,
        "userName": _user_name(user),
        "isManager": is_manager,
        "status": m.status,
        "applyTime": m.apply_time,
        "joinTime": m.join_time,
        "createTime": m.create_time,
        "updateTime": m.update_time,
    }


def serialize_member_with_user(m, user, is_manager=False) -> dict:
    return {
        "id": m.id,
        "clubId": m.club_id,
        "userId": m.user_id,
        "isManager": is_manager,
        "status": m.status,
        "applyTime": m.apply_time.isoformat() if m.apply_time is not None else None,
        "joinTime": m.join_time.isoformat() if m.join_time is not None else None,
        "user": serialize_user(user),
    }
