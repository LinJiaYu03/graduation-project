from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.exceptions import BizException
from app.models.rbac import Permission, Role, RolePermission, UserRole
from app.models.user import User


class RoleCode:
    USER = "USER"
    CLUB_MANAGER = "CLUB_MANAGER"
    ADMIN = "ADMIN"


class Perm:
    USER_UPDATE = "user:update"
    USER_VIEW = "user:view"
    USER_DELETE = "user:delete"
    USER_ROLE_ASSIGN = "user:role:assign"
    USER_MANAGE = "user:manage"

    CLUB_VIEW = "club:view"
    CLUB_CREATE = "club:create"
    CLUB_UPDATE = "club:update"
    CLUB_JOIN = "club:join"
    CLUB_MEMBER_VIEW = "club:member:view"
    CLUB_MANAGER_ASSIGN = "club:manager:assign"

    ACTIVITY_VIEW = "activity:view"
    ACTIVITY_CREATE = "activity:create"
    ACTIVITY_UPDATE = "activity:update"
    ACTIVITY_DELETE = "activity:delete"
    ACTIVITY_PUBLISH = "activity:publish"
    ACTIVITY_REVIEW = "activity:review"
    ACTIVITY_QRCODE = "activity:qrcode"
    ACTIVITY_REGISTER = "activity:register"
    ACTIVITY_COMMENT = "activity:comment"
    ACTIVITY_CHECKIN = "activity:checkin"
    ACTIVITY_STATS = "activity:stats"
    ACTIVITY_EXPORT = "activity:export"

    REGISTRATION_VIEW = "registration:view"
    REGISTRATION_REVIEW = "registration:review"

    RBAC_MANAGE = "rbac:manage"


def get_user_permission_codes(
    db: Session, user_id: int, club_id: int = 0
) -> set[str]:
    """club_id=0 只取全局角色；传入社团ID时取全局角色 + 该社团角色。"""
    query = (
        db.query(Permission.code)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(Role, Role.id == RolePermission.role_id)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id, Role.status == 1)
    )
    if club_id:
        query = query.filter(
            or_(UserRole.club_id == 0, UserRole.club_id == club_id)
        )
    else:
        query = query.filter(UserRole.club_id == 0)
    return {row[0] for row in query.distinct().all()}


def has_permission(
    db: Session, user_id: int, code: str, club_id: int = 0
) -> bool:
    return code in get_user_permission_codes(db, user_id, club_id)


def assert_permission(
    db: Session,
    user: User,
    code: str,
    club_id: int = 0,
    message: str = "无权限操作",
) -> User:
    """调用方必须保证 user 已通过 get_current_user 认证。"""
    if not has_permission(db, user.id, code, club_id):
        raise BizException(403, message)
    return user


def get_user_roles(db: Session, user_id: int) -> list[dict]:
    rows = (
        db.query(Role.code, Role.name, UserRole.club_id)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id, Role.status == 1)
        .all()
    )
    return [
        {"code": code, "name": name, "clubId": club_id}
        for code, name, club_id in rows
    ]
