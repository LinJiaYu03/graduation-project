from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import BizException
from app.core.rbac import assert_permission
from app.core.security import decode_token
from app.db.database import get_db
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)

def get_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if credentials is None:
        raise BizException(401, "请先登录")
    try:
        return decode_token(credentials.credentials, expected_type="access")
    except (ValueError, KeyError, TypeError):
        raise BizException(401, "登录状态无效，请重新登录")


def get_current_user(
    # 从请求头中获取Bearer token
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise BizException(401, "请先登录")

    try:
        # 校验
        payload = decode_token(credentials.credentials, expected_type="access")
        user_id = int(payload["sub"])
    except (ValueError, KeyError, TypeError):
        raise BizException(401, "登录状态无效，请重新登录")
    
    user = db.query(User).filter(User.id == user_id).first()
    # 校验用户是否存在 or token版本是否匹配
    if user is None or (payload.get("ver") or 0) != (user.token_version or 0):
        raise BizException(401, "登录状态已失效，请重新登录")
    return user


def require_permission(code: str):
    """全局权限依赖：仅校验 club_id=0 的全局角色。"""

    def dependency(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> User:
        assert_permission(db, current_user, code)
        return current_user

    return dependency
