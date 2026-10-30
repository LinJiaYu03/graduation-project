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


MEMBER_PENDING = 0
MEMBER_ACTIVE = 1
MEMBER_REJECTED = 2


def _manager_role(db: Session) -> Role:
    role = (
        db.query(Role)
        .filter(Role.code == RoleCode.CLUB_MANAGER, Role.status == 1)
        .first()
    )
    if role is None:
        raise BizException(500, "社团管理员角色未初始化")
    return role


def _manager_user_ids(db: Session, club_id: int) -> set[int]:
    role = _manager_role(db)
    rows = (
        db.query(UserRole.user_id)
        .filter(UserRole.club_id == club_id, UserRole.role_id == role.id)
        .all()
    )
    return {row[0] for row in rows}


def _managed_club_ids(db: Session, user_id: int) -> list[int]:
    role = _manager_role(db)
    rows = (
        db.query(UserRole.club_id)
        .filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role.id,
            UserRole.club_id > 0,
        )
        .all()
    )
    return list({row[0] for row in rows})


def _member_counts(db: Session, club_ids: list[int]) -> dict[int, int]:
    if not club_ids:
        return {}
    rows = (
        db.query(ClubMember.club_id, func.count(ClubMember.id))
        .filter(
            ClubMember.club_id.in_(club_ids),
            ClubMember.status == MEMBER_ACTIVE,
        )
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
        description=request.description,
        status=1,
    )
    db.add(club)
    db.flush()

    manager_role = _manager_role(db)

    now = datetime.now()
    db.add(
        ClubMember(
            club_id=club.id,
            user_id=current_user.id,
            status=MEMBER_ACTIVE,
            apply_time=now,
            join_time=now,
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

    if request.type and str(request.type).lower() == "management":
        club_ids = _managed_club_ids(db, current_user.id)
    else:
        club_ids = list(
            {
                row[0]
                for row in db.query(ClubMember.club_id)
                .filter(
                    ClubMember.user_id == current_user.id,
                    ClubMember.status == MEMBER_ACTIVE,
                )
                .all()
            }
        )

    if not club_ids:
        return success_response(
            data={"page": page_result(0, current, size, [])}, message="查询成功"
        )

    query = db.query(Club).filter(Club.id.in_(club_ids))
    if _has_text(request.keyword):
        kw = f"%{request.keyword}%"
        query = query.filter(
            or_(
                Club.name.like(kw),
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
    club_ids = _managed_club_ids(db, current_user.id)
    if not club_ids:
        return success_response(data={"items": []}, message="查询成功")

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
        .filter(
            ClubMember.club_id == club_id,
            ClubMember.status == MEMBER_ACTIVE,
        )
        .all()
    )
    if not members:
        return success_response(data={"items": []}, message="查询成功")

    user_ids = [m.user_id for m in members]
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    users_by_id = {u.id: u for u in users}
    manager_ids = _manager_user_ids(db, club_id)

    members.sort(
        key=lambda m: (
            m.user_id not in manager_ids,
            m.join_time or datetime.min,
        )
    )
    items = [
        serialize_member_with_user(
            m, users_by_id.get(m.user_id), m.user_id in manager_ids
        )
        for m in members
    ]
    return success_response(data={"items": items}, message="查询成功")


def pending_members(db: Session, club_id: int, current_user: User) -> dict:
    assert_permission(
        db,
        current_user,
        Perm.CLUB_MEMBER_AUDIT,
        club_id=club_id,
        message="无权限审核该社团的加入申请",
    )

    members = (
        db.query(ClubMember)
        .filter(
            ClubMember.club_id == club_id,
            ClubMember.status == MEMBER_PENDING,
        )
        .order_by(ClubMember.apply_time.asc())
        .all()
    )
    if not members:
        return success_response(data={"items": []}, message="查询成功")

    user_ids = [m.user_id for m in members]
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    users_by_id = {u.id: u for u in users}
    items = [
        serialize_member_with_user(m, users_by_id.get(m.user_id), False)
        for m in members
    ]
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
    now = datetime.now()

    if existing is not None:
        if existing.status == MEMBER_ACTIVE:
            raise ValueError("您已加入该社团")
        if existing.status == MEMBER_PENDING:
            raise ValueError("您已提交申请，请等待审核")

        existing.status = MEMBER_PENDING
        existing.apply_time = now
        existing.join_time = None
        existing.audit_user_id = None
        db.commit()
        db.refresh(existing)
        return success_response(
            data={"clubMember": serialize_club_member(existing, current_user)},
            message="重新提交申请成功",
        )

    member = ClubMember(
        club_id=club_id,
        user_id=current_user.id,
        status=MEMBER_PENDING,
        apply_time=now,
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return success_response(
        data={"clubMember": serialize_club_member(member, current_user)},
        message="申请已提交，等待审核",
    )


def audit_member(
    db: Session,
    club_id: int,
    user_id: int,
    approved: bool,
    current_user: User,
) -> dict:
    assert_permission(
        db,
        current_user,
        Perm.CLUB_MEMBER_AUDIT,
        club_id=club_id,
        message="无权限审核该社团的加入申请",
    )

    club = db.query(Club).filter(Club.id == club_id).first()
    if club is None:
        raise ValueError("社团不存在")
    if club.status is None or club.status != 1:
        raise ValueError("该社团已禁用")

    member = (
        db.query(ClubMember)
        .filter(
            ClubMember.club_id == club_id,
            ClubMember.user_id == user_id,
        )
        .first()
    )
    if member is None:
        raise ValueError("该用户未申请加入该社团")
    if member.status != MEMBER_PENDING:
        raise ValueError("该申请已处理")

    if approved:
        member.status = MEMBER_ACTIVE
        member.join_time = datetime.now()
    else:
        member.status = MEMBER_REJECTED
        member.join_time = None
    member.audit_user_id = current_user.id
    db.commit()

    return success_response(message="审核通过" if approved else "已拒绝该申请")


def quit_club(db: Session, club_id: int, current_user: User) -> dict:
    if club_id is None:
        return error_response(message="社团ID不能为空")

    member = (
        db.query(ClubMember)
        .filter(
            ClubMember.club_id == club_id,
            ClubMember.user_id == current_user.id,
            ClubMember.status == MEMBER_ACTIVE,
        )
        .first()
    )
    if member is None:
        raise ValueError("您不是该社团成员")

    role = _manager_role(db)
    manager_role = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == current_user.id,
            UserRole.role_id == role.id,
            UserRole.club_id == club_id,
        )
        .first()
    )
    if manager_role is not None:
        other_manager_count = (
            db.query(UserRole)
            .filter(
                UserRole.role_id == role.id,
                UserRole.club_id == club_id,
                UserRole.user_id != current_user.id,
            )
            .count()
        )
        if other_manager_count == 0:
            raise ValueError("社团至少保留一名管理员，请先设置其他管理员")
        db.delete(manager_role)

    db.delete(member)
    db.commit()

    return success_response(message="退出社团成功")


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
        .filter(
            ClubMember.club_id == club_id,
            ClubMember.user_id == user_id,
            ClubMember.status == MEMBER_ACTIVE,
        )
        .first()
    )
    if member is None:
        raise ValueError("该用户未加入该社团")

    role = _manager_role(db)

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
        if existing_role is not None:
            raise ValueError("该成员已是该社团的管理员")
        db.add(
            UserRole(
                user_id=user_id,
                role_id=role.id,
                club_id=club_id,
            )
        )
    else:
        if existing_role is None:
            raise ValueError("该成员不是该社团的管理员")
        other_manager_count = (
            db.query(UserRole)
            .filter(
                UserRole.role_id == role.id,
                UserRole.club_id == club_id,
                UserRole.user_id != user_id,
            )
            .count()
        )
        if other_manager_count == 0:
            raise ValueError("社团至少保留一个管理员")
        db.delete(existing_role)

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
