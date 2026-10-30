from datetime import datetime
from decimal import Decimal
from typing import Annotated, Any, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from app.utils.time_util import dt_to_millis, millis_to_dt


def _parse_dt(v: Any):
    """对齐 Jackson LocalDateTime：接受 "yyyy-MM-dd HH:mm:ss" 字符串或毫秒时间戳。"""
    if v is None:
        return None
    if isinstance(v, datetime):
        return v
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return millis_to_dt(int(v))
    s = str(v).strip()
    if s == "":
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


DateTime = Annotated[Optional[datetime], BeforeValidator(_parse_dt)]


class ActivityCreateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    activityType: Optional[str] = None
    location: Optional[str] = None
    clubId: Optional[int] = None
    notice: Optional[str] = None
    registrationStartTime: DateTime = None
    registrationEndTime: DateTime = None
    startTime: DateTime = None
    endTime: DateTime = None
    maxParticipants: Optional[int] = None
    needAudit: Optional[bool] = None
    imageUrls: Optional[list[str]] = None


class ActivityUpdateRequest(BaseModel):
    activityId: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    activityType: Optional[str] = None
    location: Optional[str] = None
    notice: Optional[str] = None
    registrationStartTime: DateTime = None
    registrationEndTime: DateTime = None
    startTime: DateTime = None
    endTime: DateTime = None
    maxParticipants: Optional[int] = None
    needAudit: Optional[bool] = None
    imageUrls: Optional[list[str]] = None


class ActivityReviewRequest(BaseModel):
    activityId: Optional[int] = None
    pass_: Optional[bool] = Field(default=None, alias="pass")
    remark: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class ActivitySearchRequest(BaseModel):
    keyword: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    currentPage: Optional[int] = None
    pageSize: Optional[int] = None


class ActivityCommentRequest(BaseModel):
    activityId: Optional[int] = None
    score: Optional[Decimal] = None
    comment: Optional[str] = None


class RegistrationReviewRequest(BaseModel):
    activityId: Optional[int] = None
    userId: Optional[int] = None
    pass_: Optional[bool] = Field(default=None, alias="pass")
    remark: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


def _number(v) -> Any:
    """对齐 Jackson BigDecimal：数字字符串/Decimal 序列化为 JSON number，不可解析时保留原值。"""
    if v is None:
        return None
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip()
    if s == "":
        return None
    try:
        f = float(s)
    except ValueError:
        return v
    return int(f) if f.is_integer() else f


def _split_urls(raw) -> list[str]:
    if raw is None:
        return []
    return [x.strip() for x in str(raw).split(",") if x.strip()]


def serialize_activity(a) -> dict | None:
    """对齐 Jackson 序列化 Activity 实体（camelCase，imageUrls 为逗号字符串，时间为 ISO 字符串）"""
    if a is None:
        return None
    return {
        "id": a.id,
        "imageUrls": a.image_urls,
        "name": a.name,
        "clubId": a.club_id,
        "description": a.description,
        "location": a.location,
        "notice": a.notice,
        "registrationStartTime": a.registration_start_time,
        "registrationEndTime": a.registration_end_time,
        "startTime": a.start_time,
        "endTime": a.end_time,
        "maxParticipants": a.max_participants,
        "currentParticipants": a.current_participants,
        "needAudit": a.need_audit,
        "activityType": a.activity_type,
        "activityLevel": a.activity_level,
        "status": a.status,
        "score": _number(a.score),
        "auditStatus": a.audit_status,
        "auditTime": a.audit_time,
        "auditUserId": a.audit_user_id,
        "isPublished": a.is_published,
        "createTime": a.create_time,
        "updateTime": a.update_time,
    }


def serialize_activity_dto(a, image_list: bool = True) -> dict | None:
    """对齐 ActivityDTO：时间字段转毫秒时间戳，imageUrls 为数组（statistics 场景下为 null）。"""
    if a is None:
        return None
    return {
        "id": a.id,
        "imageUrls": _split_urls(a.image_urls) if image_list else None,
        "name": a.name,
        "clubId": a.club_id,
        "description": a.description,
        "location": a.location,
        "notice": a.notice,
        "registrationStartTime": dt_to_millis(a.registration_start_time),
        "registrationEndTime": dt_to_millis(a.registration_end_time),
        "startTime": dt_to_millis(a.start_time),
        "endTime": dt_to_millis(a.end_time),
        "maxParticipants": a.max_participants,
        "currentParticipants": a.current_participants,
        "needAudit": a.need_audit,
        "activityType": a.activity_type,
        "activityLevel": a.activity_level,
        "status": a.status,
        "score": _number(a.score),
        "auditStatus": a.audit_status,
        "auditTime": a.audit_time,
        "auditUserId": a.audit_user_id,
        "isPublished": a.is_published,
        "createTime": a.create_time,
        "updateTime": a.update_time,
    }


def serialize_registration(r) -> dict | None:
    """对齐 Jackson 序列化 ActivityRegistration 实体（时间为 ISO 字符串）"""
    if r is None:
        return None
    return {
        "id": r.id,
        "activityId": r.activity_id,
        "userId": r.user_id,
        "status": r.status,
        "score": _number(r.score),
        "comment": r.comment,
        "checkinTime": r.checkin_time,
        "auditUserId": r.audit_user_id,
        "auditTime": r.audit_time,
        "registrationTime": r.registration_time,
        "createTime": r.create_time,
        "updateTime": r.update_time,
    }


def serialize_registration_dto(r) -> dict | None:
    """对齐 ActivityRegistrationDTO（时间字段转毫秒时间戳）"""
    if r is None:
        return None
    return {
        "id": r.id,
        "activityId": r.activity_id,
        "userId": r.user_id,
        "status": r.status,
        "score": _number(r.score),
        "checkinTime": dt_to_millis(r.checkin_time),
        "auditUserId": r.audit_user_id,
        "auditTime": dt_to_millis(r.audit_time),
        "registrationTime": dt_to_millis(r.registration_time),
        "createTime": dt_to_millis(r.create_time),
        "updateTime": dt_to_millis(r.update_time),
    }


def serialize_user_dto(u) -> dict | None:
    """对齐 UserDTO（时间字段转毫秒时间戳）"""
    if u is None:
        return None
    return {
        "id": u.id,
        "username": u.username,
        "realName": u.real_name,
        "studentNo": u.student_no,
        "gender": u.gender,
        "phone": u.phone,
        "email": u.email,
        "avatarUrl": u.avatar_url,
        "createTime": dt_to_millis(u.create_time),
        "updateTime": dt_to_millis(u.update_time),
    }


def serialize_registration_with_user(r, u) -> dict:
    """对齐 RegistrationWithUserDTO"""
    return {
        "registration": serialize_registration_dto(r),
        "user": serialize_user_dto(u),
    }
