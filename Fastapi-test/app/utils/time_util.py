from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Shanghai")


def dt_to_millis(dt: datetime | None) -> int | None:
    """LocalDateTime -> Unix 毫秒（对齐 ZoneId.systemDefault().toInstant().toEpochMilli()）"""
    if dt is None:
        return None
    return int(dt.replace(tzinfo=TZ).timestamp() * 1000)


def millis_to_dt(ms: int | None) -> datetime | None:
    """Unix 毫秒 -> 本地 LocalDateTime（naive）"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, TZ).replace(tzinfo=None)
