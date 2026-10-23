from redis.exceptions import RedisError

from app.core.exceptions import BizException
from app.core.redis_client import redis_client

LOGIN_FAIL_LIMIT = 5
LOGIN_FAIL_WINDOW_SECONDS = 10 * 60
LOGIN_LOCK_SECONDS = 10 * 60

FAIL_PREFIX = "auth:login:fail:"
LOCK_PREFIX = "auth:login:lock:"


def _account_key(username: str) -> str:
    return username.strip().lower()

# 检查登录是否被锁定
def ensure_not_locked(username: str) -> None:
    try:
        if redis_client.exists(LOCK_PREFIX + _account_key(username)):
            raise BizException(
                429, f"登录失败次数过多，请 {LOGIN_LOCK_SECONDS // 60} 分钟后再试"
            )
    except RedisError:
        return

# 记录登录失败次数
def record_login_failure(username: str) -> None:
    account = _account_key(username)
    try:
        with redis_client.pipeline(transaction=True) as pipe:
            pipe.incr(FAIL_PREFIX + account)
            pipe.expire(FAIL_PREFIX + account, LOGIN_FAIL_WINDOW_SECONDS)
            count, _ = pipe.execute()
        if int(count) >= LOGIN_FAIL_LIMIT:
            redis_client.set(LOCK_PREFIX + account, 1, ex=LOGIN_LOCK_SECONDS)
            redis_client.delete(FAIL_PREFIX + account)
    except RedisError:
        return

# 清除登录失败次数
def clear_login_failures(username: str) -> None:
    account = _account_key(username)
    try:
        redis_client.delete(FAIL_PREFIX + account, LOCK_PREFIX + account)
    except RedisError:
        return
