from datetime import datetime

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.club import Club, ClubMember
from app.models.user import User
from app.schemas.club import ClubRequest, ClubSearchRequest, JoinedClubSearchRequest
from app.schemas.club import serialize_member_with_user


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


def create_club(db: Session, request: ClubRequest) -> Club:
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
    db.commit()
    db.refresh(club)

    if request.userId is not None:
        creator = db.query(User).filter(User.id == request.userId).first()
        if creator is not None:
            member = ClubMember(
                club_id=club.id,
                user_id=request.userId,
                is_manager=True,
                join_time=datetime.now(),
            )
            db.add(member)
            db.commit()

    return club


def search_clubs(db: Session, request: ClubSearchRequest):
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
    return total, current, size, [(c, counts.get(c.id, 0)) for c in records]


def joined_clubs(db: Session, request: JoinedClubSearchRequest):
    if request.userId is None:
        raise ValueError("用户ID不能为空")

    current = request.currentPage if (request.currentPage and request.currentPage > 0) else 1
    size = request.pageSize if (request.pageSize and request.pageSize > 0) else 10

    member_query = db.query(ClubMember).filter(ClubMember.user_id == request.userId)
    if request.type and str(request.type).lower() == "management":
        member_query = member_query.filter(ClubMember.is_manager.is_(True))
    members = member_query.all()

    if not members:
        return 0, current, size, []

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
    return total, current, size, [(c, counts.get(c.id, 0)) for c in records]


def managed_clubs(db: Session, user_id) -> list[dict]:
    if user_id is None:
        raise ValueError("用户ID不能为空")

    manager_records = (
        db.query(ClubMember)
        .filter(ClubMember.user_id == user_id, ClubMember.is_manager.is_(True))
        .all()
    )
    if not manager_records:
        return []

    club_ids = list({m.club_id for m in manager_records})
    clubs = (
        db.query(Club)
        .filter(Club.id.in_(club_ids), Club.status == 1)
        .all()
    )
    return [{"text": c.name, "value": c.id} for c in clubs]


def club_members(db: Session, club_id: int) -> list[dict]:
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
    return items


def get_club(db: Session, club_id: int):
    club = db.query(Club).filter(Club.id == club_id).first()
    if club is None:
        return None, None
    counts = _member_counts(db, [club.id])
    return club, counts.get(club.id, 0)


def join_club(db: Session, club_id: int, user_id: int) -> tuple[ClubMember, User]:
    existing = (
        db.query(ClubMember)
        .filter(ClubMember.club_id == club_id, ClubMember.user_id == user_id)
        .first()
    )
    if existing is not None:
        raise ValueError("您已经加入该社团")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("用户不存在")

    member = ClubMember(
        club_id=club_id,
        user_id=user_id,
        is_manager=False,
        join_time=datetime.now(),
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member, user


def set_manager(db: Session, club_id: int, user_id: int, is_manager: bool) -> None:
    member = (
        db.query(ClubMember)
        .filter(ClubMember.club_id == club_id, ClubMember.user_id == user_id)
        .first()
    )
    if member is None:
        raise ValueError("该用户未加入该社团")
    if is_manager and member.is_manager is True:
        raise ValueError("该成员已是该社团的管理员")

    member.is_manager = is_manager
    db.commit()

    user = db.query(User).filter(User.id == user_id).first()
    if user is not None:
        if is_manager:
            user.is_manager = True
        else:
            still_manager = (
                db.query(ClubMember)
                .filter(ClubMember.user_id == user_id, ClubMember.is_manager.is_(True))
                .count()
                > 0
            )
            user.is_manager = still_manager
        db.commit()


def latest_clubs(db: Session, limit):
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
    return [(c, counts.get(c.id, 0)) for c in clubs]
