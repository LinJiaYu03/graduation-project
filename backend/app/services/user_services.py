import uuid
from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.respones import error_response, page_result, success_response
from app.models.user import User
from app.schemas.user import (
    ProfileUpdateRequest,
    PermissionUpdateRequest,
    PasswordUpdateRequest,
    serialize_user,
)

DEFAULT_AVATAR = "https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg"


def _has_text(v) -> bool:
    """对齐 Spring StringUtils.hasText"""
    return v is not None and str(v).strip() != ""


def register(db: Session, username, password) -> dict:
    if not _has_text(username) or not _has_text(password):
        raise ValueError("账号和密码不能为空")
    exists = db.query(User).filter(User.username == username).first()
    if exists is not None:
        raise ValueError("账号已存在")
    user = User(
        username=username,
        password=password,
        is_completed=False,
        is_manager=False,
        is_boss=False,
        avatar_url=DEFAULT_AVATAR,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return success_response(data={"userId": user.id}, message="注册成功")


def login(db: Session, username, password) -> dict:
    if not _has_text(username) or not _has_text(password):
        raise ValueError("账号和密码不能为空")
    user = db.query(User).filter(User.username == username).first()
    if user is None or user.password != password:
        raise ValueError("账号或密码错误")
    user.token = str(uuid.uuid4())
    db.commit()
    db.refresh(user)
    return success_response(
        data={"token": user.token, "user": serialize_user(user)}, message="登录成功"
    )


def complete_profile(db: Session, user_id: int, request: ProfileUpdateRequest) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("用户不存在")

    for attr, value in request.model_dump(exclude_none=True).items():
        if isinstance(value, str) and not value.strip():
            continue
        setattr(user, attr, value)

    user.is_completed = True
    user.complete_time = datetime.now()

    db.commit()
    db.refresh(user)
    return success_response(
        data={"user": serialize_user(user)}, message="信息完善成功"
    )


def update_permission(
    db: Session, user_id: int, request: PermissionUpdateRequest
) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("用户不存在")

    if request.is_manager is not None:
        user.is_manager = request.is_manager
    if request.is_boss is not None:
        user.is_boss = request.is_boss
    db.commit()
    db.refresh(user)
    return success_response(data={"user": serialize_user(user)}, message="权限修改成功")


def update_password(
    db: Session, user_id: int, request: PasswordUpdateRequest
) -> dict:
    if not _has_text(request.password):
        raise ValueError("密码不能为空")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("用户不存在")

    user.password = request.password
    db.commit()
    db.refresh(user)
    return success_response(data={"user": serialize_user(user)}, message="密码修改成功")


def get_users_page(db: Session, page: int, page_size: int) -> dict:
    total = db.query(User).count()
    records = (
        db.query(User).offset((page - 1) * page_size).limit(page_size).all()
    )
    return success_response(
        data={
            "page": page_result(
                total, page, page_size, [serialize_user(u) for u in records]
            )
        },
        message="查询成功",
    )


def search_users(db: Session, keyword, page: int, page_size: int) -> dict:
    query = db.query(User)
    if _has_text(keyword):
        query = query.filter(
            or_(
                User.username.like(f"%{keyword}%"),
                User.real_name.like(f"%{keyword}%"),
                User.student_no.like(f"%{keyword}%"),
            )
        )
    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()
    return success_response(
        data={
            "page": page_result(
                total, page, page_size, [serialize_user(u) for u in records]
            )
        },
        message="查询成功",
    )


def delete_user(db: Session, user_id: int) -> dict:
    query = db.query(User).filter(User.id == user_id)
    count = query.count()
    if count > 0:
        query.delete()
        db.commit()
        return success_response(message="删除成功")
    return error_response(message="用户不存在")


def delete_users(db: Session, ids: list[int]) -> dict:
    if not ids:
        return error_response(message="请提供要删除的用户ID列表")
    db.query(User).filter(User.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return success_response(message="批量删除成功")
