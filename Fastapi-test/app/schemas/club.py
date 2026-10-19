from pydantic import BaseModel
from typing import Optional

from app.schemas.user import serialize_user


class ClubRequest(BaseModel):
    iconUrl: Optional[str] = None
    name: Optional[str] = None
    tags: Optional[str] = None
    description: Optional[str] = None
    levelTag: Optional[str] = None
    userId: Optional[int] = None


class ClubSearchRequest(BaseModel):
    keyword: Optional[str] = None
    currentPage: Optional[int] = None
    pageSize: Optional[int] = None


class JoinClubRequest(BaseModel):
    clubId: Optional[int] = None
    userId: Optional[int] = None


class JoinedClubSearchRequest(BaseModel):
    userId: Optional[int] = None
    keyword: Optional[str] = None
    currentPage: Optional[int] = None
    pageSize: Optional[int] = None
    type: Optional[str] = None


def serialize_club(c, member_count=None) -> dict | None:
    if c is None:
        return None
    return {
        "id": c.id,
        "iconUrl": c.icon_url,
        "name": c.name,
        "tags": c.tags,
        "description": c.description,
        "status": c.status,
        "createTime": c.create_time,
        "updateTime": c.update_time,
        "levelTag": c.level_tag,
        "memberCount": member_count,
    }


def serialize_club_member(m) -> dict | None:
    if m is None:
        return None
    return {
        "id": m.id,
        "clubId": m.club_id,
        "userId": m.user_id,
        "userName": m.user_name,
        "isManager": m.is_manager,
        "joinTime": m.join_time,
        "createTime": m.create_time,
        "updateTime": m.update_time,
    }


def serialize_member_with_user(m, user) -> dict:
    return {
        "id": m.id,
        "clubId": m.club_id,
        "userId": m.user_id,
        "isManager": m.is_manager,
        "joinTime": m.join_time.isoformat() if m.join_time is not None else None,
        "user": serialize_user(user),
    }
