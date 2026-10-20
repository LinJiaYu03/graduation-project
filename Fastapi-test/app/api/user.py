from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.respones import success_response, error_response, page_result
from app.schemas.user import (
    RegisterRequest,
    LoginRequest,
    WxLoginRequest,
    ProfileUpdateRequest,
    PermissionUpdateRequest,
    PasswordUpdateRequest,
    serialize_user,
)
from app.services import user_services

user_router = APIRouter(tags=["users"])


@user_router.post("/api/users/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = user_services.register(db, request.username, request.password)
        return success_response(data={"userId": user.id}, message="注册成功")
    except ValueError as e:
        return error_response(message=str(e))


@user_router.post("/api/users/wx-login")
def wx_login(request: WxLoginRequest, db: Session = Depends(get_db)):
    try:
        user = user_services.wx_login(db, request.code)
        return success_response(
            data={"token": user.token, "user": serialize_user(user)}, message="登录成功"
        )
    except ValueError as e:
        return error_response(message=str(e))


@user_router.post("/api/users/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = user_services.login(db, request.username, request.password)
        return success_response(
            data={"token": user.token, "user": serialize_user(user)}, message="登录成功"
        )
    except ValueError as e:
        return error_response(message=str(e))


@user_router.get("/api/users")
def get_user_list(
    currentPage: int = 1, pageSize: int = 10, db: Session = Depends(get_db)
):
    total, records = user_services.get_users_page(db, currentPage, pageSize)
    return success_response(
        data={
            "page": page_result(
                total, currentPage, pageSize, [serialize_user(u) for u in records]
            )
        },
        message="查询成功",
    )


@user_router.get("/api/users/search")
def search_users(
    keyword: str | None = None,
    currentPage: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db),
):
    total, records = user_services.search_users(db, keyword, currentPage, pageSize)
    return success_response(
        data={
            "page": page_result(
                total, currentPage, pageSize, [serialize_user(u) for u in records]
            )
        },
        message="查询成功",
    )


@user_router.delete("/api/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        result = user_services.delete_user(db, id)
        if result:
            return success_response(message="删除成功")
        return error_response(message="用户不存在")
    except Exception as e:
        return error_response(message="删除失败: " + str(e))


@user_router.delete("/api/users")
def delete_users(ids: list[int] = Body(...), db: Session = Depends(get_db)):
    try:
        if not ids:
            return error_response(message="请提供要删除的用户ID列表")
        result = user_services.delete_users(db, ids)
        if result:
            return success_response(message="批量删除成功")
        return error_response(message="删除失败")
    except Exception as e:
        return error_response(message="批量删除失败: " + str(e))


@user_router.put("/api/users/{id}/profile")
def complete_profile(
    id: int, request: ProfileUpdateRequest, db: Session = Depends(get_db)
):
    try:
        user = user_services.complete_profile(db, id, request)
        return success_response(data={"user": serialize_user(user)}, message="信息完善成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message=str(e))


@user_router.put("/api/users/{id}/permission")
def update_permission(
    id: int, request: PermissionUpdateRequest, db: Session = Depends(get_db)
):
    try:
        user = user_services.update_permission(db, id, request)
        return success_response(data={"user": serialize_user(user)}, message="权限修改成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message=str(e))


@user_router.put("/api/users/{id}/password")
def update_password(
    id: int, request: PasswordUpdateRequest, db: Session = Depends(get_db)
):
    try:
        user = user_services.update_password(db, id, request)
        return success_response(data={"user": serialize_user(user)}, message="密码修改成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message=str(e))
