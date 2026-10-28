from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_permission
from app.core.rbac import Perm
from app.db.database import get_db
from app.core.respones import ApiResponse
from app.models.user import User
from app.schemas.rbac import UserRoleAssignRequest
from app.schemas.user import (
    RegisterRequest,
    LoginRequest,
    ProfileUpdateRequest,
    PasswordUpdateRequest,
    ProfileUpdateData,
    RefreshTokenRequest,
    TokenData,
)
from app.services import rbac_services, user_services

user_router = APIRouter()


@user_router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return user_services.register(db, request.username, request.password)


@user_router.post(
    "/login",
    response_model=ApiResponse[TokenData],
    summary="用户登录",
)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return user_services.login(db, request.username, request.password)


@user_router.post(
    "/refresh",
    response_model=ApiResponse[TokenData],
    summary="刷新令牌",
)
def refresh(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    return user_services.refresh(db, request.refresh_token)


@user_router.post("/logout", summary="退出登录")
def logout(request: RefreshTokenRequest):
    return user_services.logout(request.refresh_token)


@user_router.get(
    "/",
    dependencies=[Depends(require_permission(Perm.USER_VIEW))],
    summary="分页查询用户",
)
def get_user_list(
    currentPage: int = 1, pageSize: int = 10, db: Session = Depends(get_db)
):
    return user_services.get_users_page(db, currentPage, pageSize)


@user_router.get(
    "/search",
    dependencies=[Depends(require_permission(Perm.USER_VIEW))],
    summary="搜索用户",
)
def search_users(
    keyword: str | None = None,
    currentPage: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db),
):
    return user_services.search_users(db, keyword, currentPage, pageSize)


@user_router.delete(
    "/{id}",
    dependencies=[Depends(require_permission(Perm.USER_DELETE))],
    summary="删除用户",
)
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_services.delete_user(db, id)


@user_router.delete(
    "/",
    dependencies=[Depends(require_permission(Perm.USER_DELETE))],
    summary="批量删除用户",
)
def delete_users(ids: list[int] = Body(...), db: Session = Depends(get_db)):
    return user_services.delete_users(db, ids)


@user_router.put(
    "/profile", response_model=ApiResponse[ProfileUpdateData],
    summary="完善用户信息",
)
def complete_profile(
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_services.complete_profile(db, request, current_user)


@user_router.put(
    "/{id}/roles",
    summary="分配用户全局角色",
)
def assign_user_roles(
    id: int,
    request: UserRoleAssignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Perm.USER_ROLE_ASSIGN)),
):
    return rbac_services.assign_global_roles(db, id, request, current_user)


@user_router.put("/password", summary="修改密码")
def update_password(
    request: PasswordUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_services.update_password(db, request, current_user)
