from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.core.respones import ApiResponse
from app.models.user import User
from app.schemas.user import (
    RegisterRequest,
    LoginRequest,
    ProfileUpdateRequest,
    PasswordUpdateRequest,
    RefreshTokenRequest,
    TokenData,
    UserResponse,
)
from app.services import user_services

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
    "/profile",
    response_model=ApiResponse[UserResponse],
    summary="获取当前用户信息",
)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_services.get_profile(db, current_user)


@user_router.put("/profile", summary="完善用户信息")
def complete_profile(
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_services.complete_profile(db, request, current_user)


@user_router.put("/password", summary="修改密码")
def update_password(
    request: PasswordUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_services.update_password(db, request, current_user)
