from fastapi import APIRouter

from .activity import activity_router
from .campus import campus_router
from .club import club_router
from .user import user_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/users", tags=["用户模块"])
v1_router.include_router(activity_router, prefix="/activities", tags=["活动模块"])
v1_router.include_router(club_router, prefix="/clubs", tags=["社团模块"])
v1_router.include_router(campus_router, prefix="/campus", tags=["校园模块"])

__all__ = ["v1_router"]
