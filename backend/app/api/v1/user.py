from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.respones import ApiResponse
from app.schemas.user import (
    RegisterRequest,
    LoginRequest,
    WxLoginRequest,
    ProfileUpdateRequest,
    PermissionUpdateRequest,
    PasswordUpdateRequest,
    ProfileUpdateData,
)
from app.services import user_services

user_router = APIRouter()


@user_router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return user_services.register(db, request.username, request.password)


@user_router.post("/wx-login")
def wx_login(request: WxLoginRequest, db: Session = Depends(get_db)):
    return user_services.wx_login(db, request.code)


@user_router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return user_services.login(db, request.username, request.password)


@user_router.get("/")
def get_user_list(
    currentPage: int = 1, pageSize: int = 10, db: Session = Depends(get_db)
):
    return user_services.get_users_page(db, currentPage, pageSize)


@user_router.get("/search")
def search_users(
    keyword: str | None = None,
    currentPage: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db),
):
    return user_services.search_users(db, keyword, currentPage, pageSize)


@user_router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_services.delete_user(db, id)


@user_router.delete("/")
def delete_users(ids: list[int] = Body(...), db: Session = Depends(get_db)):
    return user_services.delete_users(db, ids)


@user_router.put(
    "{id}/profile", response_model=ApiResponse[ProfileUpdateData],
    summary="完善用户信息",
)
def complete_profile(
    id: int, request: ProfileUpdateRequest, db: Session = Depends(get_db)
):
    return user_services.complete_profile(db, id, request)


@user_router.put("{id}/permission")
def update_permission(
    id: int, request: PermissionUpdateRequest, db: Session = Depends(get_db)
):
    return user_services.update_permission(db, id, request)


@user_router.put("{id}/password")
def update_password(
    id: int, request: PasswordUpdateRequest, db: Session = Depends(get_db)
):
    return user_services.update_password(db, id, request)
