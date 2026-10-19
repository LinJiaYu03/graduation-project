import uuid
import httpx
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.club import ClubMember
from app.schemas.user import ProfileUpdateRequest

DEFAULT_AVATAR = "https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg"
WX_APPID = "wx2caaaf47aead807a"
WX_SECRET = "1e6dcbf6a9ccfc823a5447aa262adcc2"


def _has_text(v) -> bool:
    """对齐 Spring StringUtils.hasText"""
    return v is not None and str(v).strip() != ""


def register(db: Session, username, password) -> User:
    if not _has_text(username) or not _has_text(password):
        raise ValueError("账号和密码不能为空")
    exists = db.query(User).filter(User.username == username).first()
    if exists is not None:
        raise ValueError("账号已存在")
    user = User(
        username=username,
        password=password,
        is_completed=False,
        is_manager=False,
        is_boss=False,
        avatar_url=DEFAULT_AVATAR,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, username, password) -> User:
    if not _has_text(username) or not _has_text(password):
        raise ValueError("账号和密码不能为空")
    user = db.query(User).filter(User.username == username).first()
    if user is None or user.password != password:
        raise ValueError("账号或密码错误")
    user.token = str(uuid.uuid4())
    db.commit()
    db.refresh(user)
    return user


def wx_login(db: Session, code) -> User:
    if not _has_text(code):
        raise ValueError("code不能为空")
    url = (
        "https://api.weixin.qq.com/sns/jscode2session"
        f"?appid={WX_APPID}&secret={WX_SECRET}&js_code={code}&grant_type=authorization_code"
    )
    resp = httpx.get(url, timeout=10)
    data = resp.json()
    if data.get("errcode") and data.get("errcode") != 0:
        raise ValueError("微信登录失败: " + str(data.get("errmsg", "未知错误")))
    openid = data.get("openid")
    if not _has_text(openid):
        raise ValueError("无法获取OpenID")

    user = db.query(User).filter(User.wx_openid == openid).first()
    if user is None:
        user = User(
            wx_openid=openid,
            username="wx_" + str(uuid.uuid4())[:8],
            password=str(uuid.uuid4()),
            is_completed=False,
            is_manager=False,
            is_boss=False,
            avatar_url=DEFAULT_AVATAR,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    user.token = str(uuid.uuid4())
    db.commit()
    db.refresh(user)
    return user


def complete_profile(db: Session, user_id: int, request: ProfileUpdateRequest) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("用户不存在")

    real_name_changed = False
    if _has_text(request.realName):
        old_real_name = user.real_name
        user.real_name = request.realName
        if old_real_name != request.realName:
            real_name_changed = True
    if _has_text(request.studentNo):
        user.student_no = request.studentNo
    if request.gender is not None:
        user.gender = request.gender
    if _has_text(request.phone):
        user.phone = request.phone
    if _has_text(request.email):
        user.email = request.email
    if _has_text(request.schoolName):
        user.school_name = request.schoolName
    if _has_text(request.collegeName):
        user.college_name = request.collegeName
    if _has_text(request.className):
        user.class_name = request.className
    if _has_text(request.avatarUrl):
        user.avatar_url = request.avatarUrl
    if request.isManager is not None:
        user.is_manager = request.isManager
    if request.isBoss is not None:
        user.is_boss = request.isBoss
    if _has_text(request.password):
        user.password = request.password

    user.is_completed = True
    from datetime import datetime

    user.complete_time = datetime.now()
    db.commit()
    db.refresh(user)

    if real_name_changed:
        user_name = user.real_name if _has_text(user.real_name) else user.username
        db.query(ClubMember).filter(ClubMember.user_id == user_id).update(
            {ClubMember.user_name: user_name}
        )
        db.commit()

    return user


def get_users_page(db: Session, page: int, page_size: int):
    total = db.query(User).count()
    records = (
        db.query(User).offset((page - 1) * page_size).limit(page_size).all()
    )
    return total, records


def search_users(db: Session, keyword, page: int, page_size: int):
    query = db.query(User)
    if _has_text(keyword):
        query = query.filter(
            or_(
                User.username.like(f"%{keyword}%"),
                User.real_name.like(f"%{keyword}%"),
                User.student_no.like(f"%{keyword}%"),
            )
        )
    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()
    return total, records


def delete_user(db: Session, user_id: int) -> bool:
    query = db.query(User).filter(User.id == user_id)
    count = query.count()
    if count > 0:
        query.delete()
        db.commit()
    return count > 0


def delete_users(db: Session, ids: list[int]) -> bool:
    if not ids:
        return False
    db.query(User).filter(User.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return True
