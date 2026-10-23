from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class LoginRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class ProfileUpdateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    real_name: Optional[str] = None
    student_no: Optional[str] = None
    gender: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    school_name: Optional[str] = None
    college_name: Optional[str] = None
    class_name: Optional[str] = None
    avatar_url: Optional[str] = None


class PermissionUpdateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    is_manager: Optional[bool] = None
    is_boss: Optional[bool] = None


class PasswordUpdateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    old_password: Optional[str] = None
    password: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    refresh_token: Optional[str] = None


class UserResponse(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    wxOpenid: Optional[str] = None
    isCompleted: Optional[bool] = None
    realName: Optional[str] = None
    studentNo: Optional[str] = None
    gender: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    schoolName: Optional[str] = None
    collegeName: Optional[str] = None
    className: Optional[str] = None
    completeTime: Optional[datetime] = None
    isManager: Optional[bool] = None
    isBoss: Optional[bool] = None
    avatarUrl: Optional[str] = None
    token: Optional[str] = None
    createTime: Optional[datetime] = None
    updateTime: Optional[datetime] = None


class ProfileUpdateData(BaseModel):
    user: Optional[UserResponse] = None


class TokenData(BaseModel):
    token: Optional[str] = None
    accessToken: Optional[str] = None
    refreshToken: Optional[str] = None
    tokenType: Optional[str] = None
    expiresIn: Optional[int] = None
    user: Optional[UserResponse] = None


def serialize_user(u) -> dict | None:
    if u is None:
        return None
    return {
        "id": u.id,
        "username": u.username,
        "wxOpenid": u.wx_openid,
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
        "token": None,
        "createTime": u.create_time,
        "updateTime": u.update_time,
    }
