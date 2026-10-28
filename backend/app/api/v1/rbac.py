from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_permission
from app.core.rbac import Perm
from app.db.database import get_db
from app.models.user import User
from app.schemas.rbac import RolePermissionUpdateRequest
from app.services import rbac_services

rbac_router = APIRouter()


@rbac_router.get(
    "/roles",
    dependencies=[Depends(require_permission(Perm.RBAC_MANAGE))],
    summary="角色列表",
)
def get_roles(db: Session = Depends(get_db)):
    return rbac_services.list_roles(db)


@rbac_router.get(
    "/permissions",
    dependencies=[Depends(require_permission(Perm.RBAC_MANAGE))],
    summary="权限列表",
)
def get_permissions(db: Session = Depends(get_db)):
    return rbac_services.list_permissions(db)


@rbac_router.put(
    "/roles/{roleId}/permissions",
    summary="配置角色权限",
)
def update_role_permissions(
    roleId: int,
    request: RolePermissionUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Perm.RBAC_MANAGE)),
):
    return rbac_services.update_role_permissions(db, roleId, request, current_user)


@rbac_router.get("/me", summary="当前用户角色与权限")
def get_my_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rbac_services.get_my_permissions(db, current_user)
