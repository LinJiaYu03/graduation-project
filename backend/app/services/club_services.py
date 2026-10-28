from datetime import datetime

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.core.exceptions import BizException
from app.core.rbac import Perm, RoleCode, assert_permission
from app.core.respones import error_response, page_result, success_response
from app.models.club import Club, ClubMember
from app.models.rbac import Role, UserRole
from app.models.user import User
from app.schemas.club import (
    ClubRequest,
    ClubSearchRequest,
    JoinedClubSearchRequest,
    serialize_club,
    serialize_club_member,
    serialize_member_with_user,
)


def _has_text(v) -> bool:
    return v is not None and str(v).strip() != ""


def _member_counts(db: Session, club_ids: list[int]) -> dict[int, int]:
    if not club_ids:
        return {}
    rows = (
        db.query(ClubMember.club_id, func.count(ClubMember.id))
        .filter(ClubMember.club_id.in_(club_ids))
        .group_by(ClubMember.club_id)
        .all()
    )
    return {row[0]: row[1] for row in rows}


def create_club(
    db: Session, request: ClubRequest, current_user: User
) -> dict:
    if not _has_text(request.name):
        raise ValueError("社团名称不能为空")

    club = Club(
        icon_url=request.iconUrl,
        name=request.name,
        tags=request.tags,
        description=request.description,
        level_tag=request.levelTag,
        status=1,
    )
    db.add(club)
    db.flush()

    manager_role = (
        db.query(Role)
        .filter(Role.code == RoleCode.CLUB_MANAGER, Role.status == 1)
        .first()
    )
    if manager_role is None:
        raise BizException(500, "社团管理员角色未初始化")

    db.add(
        ClubMember(
            club_id=club.id,
            user_id=current_user.id,
            is_manager=True,
            join_time=datetime.now(),
        )
    )
    db.add(
        UserRole(
            user_id=current_user.id,
            role_id=manager_role.id,
            club_id=club.id,
        )
    )
    db.commit()
    db.refresh(club)

    return success_response(
        data={"club": serialize_club(club), "clubId": club.id}, message="创建社团成功"
    )


def search_clubs(db: Session, request: ClubSearchRequest) -> dict:
    current = request.currentPage if (request.currentPage and request.currentPage > 0) else 1
    size = request.pageSize if (request.pageSize and request.pageSize > 0) else 10

    query = db.query(Club).filter(Club.status == 1)
    if _has_text(request.keyword):
        kw = f"%{request.keyword}%"
        query = query.filter(
            or_(
                Club.name.like(kw),
                Club.tags.like(kw),
                Club.description.like(kw),
            )
        )
    query = query.order_by(Club.create_time.desc())

    total = query.count()
    records = query.offset((current - 1) * size).limit(size).all()
    counts = _member_counts(db, [c.id for c in records])
    return success_response(
        data={
            "page": page_result(
                total, current, size, [serialize_club(c, counts.get(c.id, 0)) for c in records]
            )
        },
        message="查询成功",
    )


def joined_clubs(
    db: Session, request: JoinedClubSearchRequest, current_user: User
) -> dict:
    current = request.currentPage if (request.currentPage and request.currentPage > 0) else 1
    size = request.pageSize if (request.pageSize and request.pageSize > 0) else 10

    member_query = db.query(ClubMember).filter(ClubMember.user_id == current_user.id)
    if request.type and str(request.type).lower() == "management":
        member_query = member_query.filter(ClubMember.is_manager.is_(True))
    members = member_query.all()

    if not members:
        return success_response(
            data={"page": page_result(0, current, size, [])}, message="查询成功"
        )

    club_ids = list({m.club_id for m in members})

    query = db.query(Club).filter(Club.id.in_(club_ids))
    if _has_text(request.keyword):
        kw = f"%{request.keyword}%"
        query = query.filter(
            or_(
                Club.name.like(kw),
                Club.tags.like(kw),
                Club.description.like(kw),
            )
        )
    query = query.filter(Club.status == 1).order_by(Club.create_time.desc())

    total = query.count()
    records = query.offset((current - 1) * size).limit(size).all()
    counts = _member_counts(db, [c.id for c in records])
    return success_response(
        data={
            "page": page_result(
                total, current, size, [serialize_club(c, counts.get(c.id, 0)) for c in records]
            )
        },
        message="查询成功",
    )


def managed_clubs(db: Session, current_user: User) -> dict:
    manager_records = (
        db.query(ClubMember)
        .filter(
            ClubMember.user_id == current_user.id,
            ClubMember.is_manager.is_(True),
        )
        .all()
    )
    if not manager_records:
        return success_response(data={"items": []}, message="查询成功")

    club_ids = list({m.club_id for m in manager_records})
    clubs = (
        db.query(Club)
        .filter(Club.id.in_(club_ids), Club.status == 1)
        .all()
    )
    return success_response(
        data={"items": [{"text": c.name, "value": c.id} for c in clubs]},
        message="查询成功",
    )


def club_members(db: Session, club_id: int) -> dict:
    members = (
        db.query(ClubMember)
        .filter(ClubMember.club_id == club_id)
        .order_by(ClubMember.is_manager.desc(), ClubMember.join_time.asc())
        .all()
    )
    items = []
    for m in members:
        user = db.query(User).filter(User.id == m.user_id).first()
        items.append(serialize_member_with_user(m, user))
    return success_response(data={"items": items}, message="查询成功")


def get_club(db: Session, club_id: int) -> dict:
    club = db.query(Club).filter(Club.id == club_id).first()
    if club is None:
        return error_response(message="社团不存在")
    counts = _member_counts(db, [club.id])
    return success_response(
        data={"club": serialize_club(club, counts.get(club.id, 0))}, message="查询成功"
    )


def join_club(db: Session, club_id: int, current_user: User) -> dict:
    if club_id is None:
        return error_response(message="社团ID不能为空")

    club = db.query(Club).filter(Club.id == club_id).first()
    if club is None:
        return error_response(message="社团不存在")
    if club.status is None or club.status != 1:
        return error_response(message="该社团已禁用")

    existing = (
        db.query(ClubMember)
        .filter(
            ClubMember.club_id == club_id,
            ClubMember.user_id == current_user.id,
        )
        .first()
    )
    if existing is not None:
        raise ValueError("您已经加入该社团")

    member = ClubMember(
        club_id=club_id,
        user_id=current_user.id,
        is_manager=False,
        join_time=datetime.now(),
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return success_response(
        data={"clubMember": serialize_club_member(member, current_user)},
        message="加入社团成功",
    )


def set_manager(
    db: Session,
    club_id: int,
    user_id: int,
    is_manager: bool,
    current_user: User,
) -> dict:
    assert_permission(
        db,
        current_user,
        Perm.CLUB_MANAGER_ASSIGN,
        club_id=club_id,
        message="无权限设置该社团管理员",
    )

    member = (
        db.query(ClubMember)
        .filter(ClubMember.club_id == club_id, ClubMember.user_id == user_id)
        .first()
    )
    if member is None:
        raise ValueError("该用户未加入该社团")

    role = (
        db.query(Role)
        .filter(Role.code == RoleCode.CLUB_MANAGER, Role.status == 1)
        .first()
    )
    if role is None:
        raise BizException(500, "社团管理员角色未初始化")

    existing_role = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role.id,
            UserRole.club_id == club_id,
        )
        .first()
    )

    if is_manager:
        if member.is_manager is True and existing_role is not None:
            raise ValueError("该成员已是该社团的管理员")
        if existing_role is None:
            db.add(
                UserRole(
                    user_id=user_id,
                    role_id=role.id,
                    club_id=club_id,
                )
            )
    else:
        other_manager_count = (
            db.query(ClubMember)
            .filter(
                ClubMember.club_id == club_id,
                ClubMember.is_manager.is_(True),
                ClubMember.user_id != user_id,
            )
            .count()
        )
        if member.is_manager is True and other_manager_count == 0:
            raise ValueError("社团至少保留一个管理员")
        if existing_role is not None:
            db.delete(existing_role)

    member.is_manager = is_manager
    db.commit()

    return success_response(
        message="设置管理员成功" if is_manager else "取消管理员成功"
    )


def latest_clubs(db: Session, limit) -> dict:
    if limit is None or limit <= 0:
        limit = 4
    clubs = (
        db.query(Club)
        .filter(Club.status == 1)
        .order_by(Club.create_time.desc())
        .limit(limit)
        .all()
    )
    counts = _member_counts(db, [c.id for c in clubs])
    return success_response(
        data={"items": [serialize_club(c, counts.get(c.id, 0)) for c in clubs]},
        message="查询成功",
    )
