from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class LoginRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class WxLoginRequest(BaseModel):
    code: Optional[str] = None


class ProfileUpdateRequest(BaseModel):
    realName: Optional[str] = None
    studentNo: Optional[str] = None
    gender: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    schoolName: Optional[str] = None
    collegeName: Optional[str] = None
    className: Optional[str] = None
    avatarUrl: Optional[str] = None
    isManager: Optional[bool] = None
    isBoss: Optional[bool] = None
    password: Optional[str] = None


def serialize_user(u) -> dict | None:
    """对齐 Jackson 序列化 User 实体的字段（camelCase）"""
    if u is None:
        return None
    return {
        "id": u.id,
        "username": u.username,
        "wxOpenid": u.wx_openid,
        "password": u.password,
        "isCompleted": u.is_completed,
        "realName": u.real_name,
        "studentNo": u.student_no,
        "gender": u.gender,
        "phone": u.phone,
        "email": u.email,
        "schoolName": u.school_name,
        "collegeName": u.college_name,
        "className": u.class_name,
        "completeTime": u.complete_time,
        "isManager": u.is_manager,
        "isBoss": u.is_boss,
        "avatarUrl": u.avatar_url,
        "token": u.token,
        "createTime": u.create_time,
        "updateTime": u.update_time,
    }
