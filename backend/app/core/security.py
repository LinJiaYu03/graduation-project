import uuid
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, stored: str | None) -> bool:
    if not stored:
        return False
    try:
        return password_hash.verify(password, stored)
    except Exception:
        return False


def _create_token(user, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id), # 用户ID
        "type": token_type, # token类型
        "ver": user.token_version or 0, # token版本
        "jti": uuid.uuid4().hex, # token uuid
        "iat": now, # 发布时间
        "exp": now + expires_delta, # 过期时间
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def create_access_token(user) -> tuple[str, int]:
    """返回 (access_token, 过期秒数)"""
    expires_in = settings.access_token_expire_minutes * 60
    token = _create_token(user, "access", timedelta(seconds=expires_in))
    return token, expires_in


def create_refresh_token(user) -> str:
    return _create_token(
        user, "refresh", timedelta(days=settings.refresh_token_expire_days)
    )


# 校验token
def decode_token(token: str, expected_type: str | None = None) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError:
        raise ValueError("登录已过期")
    except jwt.InvalidTokenError:
        raise ValueError("无效的登录凭证")

    if expected_type and payload.get("type") != expected_type:
        raise ValueError("登录凭证类型错误")
    return payload
