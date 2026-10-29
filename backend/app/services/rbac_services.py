from sqlalchemy.orm import Session

from app.core.exceptions import BizException
from app.core.rbac import (
    Perm,
    RoleCode,
    assert_permission,
    get_user_permission_codes,
    get_user_roles,
)
from app.core.respones import success_response
from app.models.rbac import Permission, Role, RolePermission, UserRole
from app.models.user import User
from app.schemas.rbac import RolePermissionUpdateRequest, UserRoleAssignRequest
from app.schemas.user import serialize_user


def assign_global_roles(
    db: Session,
    user_id: int,
    request: UserRoleAssignRequest,
    current_user: User,
) -> dict:
    assert_permission(db, current_user, Perm.USER_ROLE_ASSIGN)

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise BizException(400, "用户不存在")

    codes = list(dict.fromkeys(request.roleCodes or []))
    if not codes:
        raise BizException(400, "至少分配一个角色")

    roles = (
        db.query(Role)
        .filter(Role.code.in_(codes), Role.status == 1)
        .all()
    )
    if len(roles) != len(codes):
        raise BizException(400, "存在无效角色")
    if any(role.code == RoleCode.CLUB_MANAGER for role in roles):
        raise BizException(400, "社团管理员请通过社团成员接口设置")

    # 只替换全局角色，不动 club_id > 0 的社团角色
    db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.club_id == 0,
    ).delete(synchronize_session=False)

    for role in roles:
        db.add(UserRole(user_id=user_id, role_id=role.id, club_id=0))

    db.flush()

    admin_count = (
        db.query(UserRole)
        .join(Role, Role.id == UserRole.role_id)
        .filter(Role.code == RoleCode.ADMIN, UserRole.club_id == 0)
        .count()
    )
    if admin_count == 0:
        raise BizException(400, "系统至少保留一个超级管理员")

    db.commit()
    db.refresh(user)
    user_roles = get_user_roles(db, user_id)
    permissions = sorted(get_user_permission_codes(db, user_id))
    user_data = serialize_user(user, roles=user_roles)
    user_data["permissions"] = permissions
    return success_response(
        data={"user": user_data},
        message="角色分配成功",
    )


def list_roles(db: Session) -> dict:
    roles = db.query(Role).order_by(Role.id.asc()).all()
    items = []
    for role in roles:
        permission_codes = [
            row[0]
            for row in (
                db.query(Permission.code)
                .join(RolePermission, RolePermission.permission_id == Permission.id)
                .filter(RolePermission.role_id == role.id)
                .all()
            )
        ]
        items.append(
            {
                "id": role.id,
                "code": role.code,
                "name": role.name,
                "description": role.description,
                "status": role.status,
                "permissions": permission_codes,
            }
        )
    return success_response(data={"items": items}, message="查询成功")


def list_permissions(db: Session) -> dict:
    items = [
        {
            "id": p.id,
            "code": p.code,
            "name": p.name,
            "resource": p.resource,
            "action": p.action,
            "description": p.description,
        }
        for p in db.query(Permission)
        .order_by(Permission.resource.asc(), Permission.action.asc())
        .all()
    ]
    return success_response(data={"items": items}, message="查询成功")


def update_role_permissions(
    db: Session,
    role_id: int,
    request: RolePermissionUpdateRequest,
    current_user: User,
) -> dict:
    assert_permission(db, current_user, Perm.RBAC_MANAGE)

    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise BizException(400, "角色不存在")
    if role.code == RoleCode.ADMIN:
        raise BizException(400, "超级管理员权限不允许修改")

    codes = list(dict.fromkeys(request.permissionCodes or []))
    permissions = (
        db.query(Permission).filter(Permission.code.in_(codes)).all()
        if codes
        else []
    )
    if len(permissions) != len(codes):
        raise BizException(400, "存在无效权限")

    db.query(RolePermission).filter(
        RolePermission.role_id == role_id
    ).delete(synchronize_session=False)
    for permission in permissions:
        db.add(RolePermission(role_id=role_id, permission_id=permission.id))
    db.commit()
    return success_response(message="角色权限更新成功")


def get_my_permissions(db: Session, current_user: User) -> dict:
    return success_response(
        data={
            "roles": get_user_roles(db, current_user.id),
            "permissions": sorted(get_user_permission_codes(db, current_user.id)),
        },
        message="查询成功",
    )
