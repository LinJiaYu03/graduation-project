from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.exceptions import BizException
from app.core.login_guard import (
    clear_login_failures,
    ensure_not_locked,
    record_login_failure,
)
from app.core.rbac import (
    RoleCode,
    get_user_permission_codes,
    get_user_roles,
)
from app.core.respones import error_response, page_result, success_response
from app.core.security import (
    create_token_pair,
    decode_token,
    hash_password,
    verify_password,
)
from app.core.token_blacklist import blacklist_refresh, consume_refresh_jti
from app.models.rbac import Role, UserRole
from app.models.user import User
from app.schemas.user import (
    ProfileUpdateRequest,
    PasswordUpdateRequest,
    serialize_user,
)

DEFAULT_AVATAR = "https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg"


def _has_text(v) -> bool:
    """对齐 Spring StringUtils.hasText"""
    return v is not None and str(v).strip() != ""


def _token_response(
    db: Session, user: User, message: str = "登录成功"
) -> dict:
    access_token, refresh_token, expires_in = create_token_pair(user)
    roles = get_user_roles(db, user.id)
    permissions = sorted(get_user_permission_codes(db, user.id))
    user_data = serialize_user(user, roles=roles, permissions=permissions)
    # 兼容旧前端：仍从 user.token 读取令牌
    user_data["token"] = access_token
    return success_response(
        data={
            "token": access_token,
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "tokenType": "Bearer",
            "expiresIn": expires_in,
            "user": user_data,
        },
        message=message,
    )


def register(db: Session, username, password) -> dict:
    if not _has_text(username) or not _has_text(password):
        raise ValueError("账号和密码不能为空")
    exists = db.query(User).filter(User.username == username).first()
    if exists is not None:
        raise ValueError("账号已存在")
    user = User(
        username=username,
        password=hash_password(password),
        is_completed=False,
        avatar_url=DEFAULT_AVATAR,
    )
    db.add(user)
    db.flush()

    role = (
        db.query(Role)
        .filter(Role.code == RoleCode.USER, Role.status == 1)
        .first()
    )
    if role is None:
        raise BizException(500, "系统角色未初始化")
    db.add(UserRole(user_id=user.id, role_id=role.id, club_id=0))

    db.commit()
    db.refresh(user)
    return success_response(data={"userId": user.id}, message="注册成功")


def login(db: Session, username, password) -> dict:
    if not _has_text(username) or not _has_text(password):
        raise ValueError("账号和密码不能为空")
    ensure_not_locked(username)
    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(password, user.password):
        record_login_failure(username)
        raise ValueError("账号或密码错误")

    clear_login_failures(username)
    return _token_response(db, user, message="登录成功")


def refresh(db: Session, refresh_token) -> dict:
    if not _has_text(refresh_token):
        raise BizException(401, "refreshToken 不能为空")

    try:
        payload = decode_token(refresh_token, expected_type="refresh")
        user_id = int(payload["sub"])
    except (ValueError, KeyError, TypeError):
        raise BizException(401, "刷新凭证无效，请重新登录")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or (payload.get("ver") or 0) != (user.token_version or 0):
        raise BizException(401, "登录状态已失效，请重新登录")

    consume_refresh_jti(payload)
    return _token_response(db, user, message="刷新成功")


def logout(refresh_token) -> dict:
    """退出登录：吊销前端传入的 refresh 令牌"""
    if not _has_text(refresh_token):
        raise BizException(401, "refreshToken 不能为空")

    try:
        payload = decode_token(refresh_token, expected_type="refresh")
    except (ValueError, KeyError, TypeError):
        # 令牌已过期或非法时无需吊销，按已退出处理，保证登出幂等
        return success_response(message="退出登录成功")

    blacklist_refresh(payload)
    return success_response(message="退出登录成功")


def complete_profile(
    db: Session, request: ProfileUpdateRequest, current_user: User
) -> dict:
    for attr, value in request.model_dump(exclude_none=True).items():
        if isinstance(value, str) and not value.strip():
            continue
        setattr(current_user, attr, value)

    current_user.is_completed = True
    current_user.complete_time = datetime.now()

    db.commit()
    db.refresh(current_user)
    roles = get_user_roles(db, current_user.id)
    permissions = sorted(get_user_permission_codes(db, current_user.id))
    return success_response(
        data={
            "user": serialize_user(
                current_user, roles=roles, permissions=permissions
            )
        },
        message="信息完善成功",
    )


def update_password(
    db: Session, request: PasswordUpdateRequest, current_user: User
) -> dict:
    if not _has_text(request.password):
        raise ValueError("密码不能为空")
    if not _has_text(request.old_password):
        raise ValueError("旧密码不能为空")
    if not verify_password(request.old_password, current_user.password):
        raise ValueError("旧密码错误")

    current_user.password = hash_password(request.password)
    # 改密后使已签发的令牌全部失效
    current_user.token_version = (current_user.token_version or 0) + 1
    db.commit()
    db.refresh(current_user)
    roles = get_user_roles(db, current_user.id)
    permissions = sorted(get_user_permission_codes(db, current_user.id))
    return success_response(
        data={
            "user": serialize_user(
                current_user, roles=roles, permissions=permissions
            )
        },
        message="密码修改成功",
    )


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
