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


def _create_token(
    user,
    token_type: str,
    expires_delta: timedelta,
    token_id: str | None = None,
    extra: dict | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),  # 用户ID
        "type": token_type,  # token类型
        "ver": user.token_version or 0,  # token版本
        "jti": token_id or uuid.uuid4().hex,  # token uuid
        "iat": now,  # 发布时间
        "exp": now + expires_delta,  # 过期时间
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_token_pair(user) -> tuple[str, str, int]:
    """返回 (access_token, refresh_token, expires_in)，同一会话共用 sid"""
    now = datetime.now(timezone.utc)
    refresh_delta = timedelta(days=settings.refresh_token_expire_days)
    sid = uuid.uuid4().hex
    # refresh 的 jti 即会话标识 sid，登出时可凭 access 里的 sid 吊销
    refresh_token = _create_token(user, "refresh", refresh_delta, token_id=sid)

    expires_in = settings.access_token_expire_minutes * 60
    access_token = _create_token(
        user,
        "access",
        timedelta(seconds=expires_in),
        extra={
            "sid": sid,
            "sexp": int((now + refresh_delta).timestamp()),
        },
    )
    return access_token, refresh_token, expires_in


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
