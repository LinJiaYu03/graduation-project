import time

from redis.exceptions import RedisError

from app.core.exceptions import BizException
from app.core.redis_client import redis_client

REFRESH_BLACKLIST_PREFIX = "auth:blacklist:refresh:"


def consume_refresh_jti(payload: dict) -> None:
    """原子消费 refresh 的 jti，已使用过的令牌直接拒绝"""
    jti = payload.get("jti")
    if not jti:
        raise BizException(401, "刷新凭证无效，请重新登录")

    ttl = max(int(payload.get("exp", 0) - time.time()), 1)
    try:
        created = redis_client.set(
            f"{REFRESH_BLACKLIST_PREFIX}{jti}", 1, nx=True, ex=ttl
        )
    except RedisError:
        raise BizException(503, "服务暂不可用，请稍后重试")

    if not created:
        raise BizException(401, "刷新凭证已失效，请重新登录")


def blacklist_refresh(payload: dict) -> None:
    """主动吊销 refresh 令牌（登出等场景），不要求首次使用"""
    jti = payload.get("jti")
    if not jti:
        return

    ttl = max(int(payload.get("exp", 0) - time.time()), 1)
    try:
        redis_client.set(f"{REFRESH_BLACKLIST_PREFIX}{jti}", 1, ex=ttl)
    except RedisError:
        raise BizException(503, "服务暂不可用，请稍后重试")
