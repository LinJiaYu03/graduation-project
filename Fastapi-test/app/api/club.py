from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.respones import success_response, error_response, page_result
from app.schemas.club import (
    ClubRequest,
    ClubSearchRequest,
    JoinClubRequest,
    JoinedClubSearchRequest,
    serialize_club,
    serialize_club_member,
)
from app.services import club_services

club_router = APIRouter(tags=["clubs"])


@club_router.post("/api/clubs")
def create_club(request: ClubRequest, db: Session = Depends(get_db)):
    try:
        club = club_services.create_club(db, request)
        return success_response(
            data={"club": serialize_club(club), "clubId": club.id}, message="创建社团成功"
        )
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="创建社团失败: " + str(e))


@club_router.post("/api/clubs/search")
def search_clubs(request: ClubSearchRequest, db: Session = Depends(get_db)):
    total, current, size, records = club_services.search_clubs(db, request)
    return success_response(
        data={
            "page": page_result(
                total, current, size, [serialize_club(c, n) for c, n in records]
            )
        },
        message="查询成功",
    )


@club_router.post("/api/clubs/join")
def join_club(request: JoinClubRequest, db: Session = Depends(get_db)):
    if request.clubId is None:
        return error_response(message="社团ID不能为空")
    if request.userId is None:
        return error_response(message="用户ID不能为空")
    try:
        club = db.query(club_services.Club).filter(club_services.Club.id == request.clubId).first()
        if club is None:
            return error_response(message="社团不存在")
        if club.status is None or club.status != 1:
            return error_response(message="该社团已禁用")
        member = club_services.join_club(db, request.clubId, request.userId)
        return success_response(
            data={"clubMember": serialize_club_member(member)}, message="加入社团成功"
        )
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="加入社团失败: " + str(e))


@club_router.post("/api/clubs/joined")
def get_joined_clubs(request: JoinedClubSearchRequest, db: Session = Depends(get_db)):
    try:
        total, current, size, records = club_services.joined_clubs(db, request)
        return success_response(
            data={
                "page": page_result(
                    total, current, size, [serialize_club(c, n) for c, n in records]
                )
            },
            message="查询成功",
        )
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@club_router.get("/api/clubs/managed")
def get_managed_clubs(userId: int, db: Session = Depends(get_db)):
    try:
        items = club_services.managed_clubs(db, userId)
        return success_response(data={"items": items}, message="查询成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@club_router.get("/api/clubs/latest")
def get_latest_clubs(limit: int = 4, db: Session = Depends(get_db)):
    records = club_services.latest_clubs(db, limit)
    return success_response(
        data={"items": [serialize_club(c, n) for c, n in records]}, message="查询成功"
    )


@club_router.get("/api/clubs/{clubId}/members")
def get_club_members(clubId: int, db: Session = Depends(get_db)):
    items = club_services.club_members(db, clubId)
    return success_response(data={"items": items}, message="查询成功")


@club_router.post("/api/clubs/{clubId}/members/{userId}/manager")
def set_club_member_manager(
    clubId: int, userId: int, isManager: bool = True, db: Session = Depends(get_db)
):
    try:
        club_services.set_manager(db, clubId, userId, isManager)
        return success_response(
            message="设置管理员成功" if isManager else "取消管理员成功"
        )
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="操作失败: " + str(e))


@club_router.get("/api/clubs/{id}")
def get_club_by_id(id: int, db: Session = Depends(get_db)):
    try:
        club, member_count = club_services.get_club(db, id)
        if club is None:
            return error_response(message="社团不存在")
        return success_response(
            data={"club": serialize_club(club, member_count)}, message="查询成功"
        )
    except Exception as e:
        return error_response(message="查询失败: " + str(e))
