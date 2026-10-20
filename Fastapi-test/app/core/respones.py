from typing import Any
import math


def success_response(data: Any | None = None, message: str = "响应成功") -> dict:
    return {
        "code": 200,
        "message": message,
        "success": True,
        "data": data if data is not None else {},
    }


def error_response(code: int = 400, message: str = "响应失败", data: Any | None = None) -> dict:
    return {
        "code": code,
        "message": message,
        "success": False,
        "data": data if data is not None else {},
    }


def page_result(total: int, current_page: int, page_size: int, records: list) -> dict:
    total_page = math.ceil(total / page_size) if page_size else 0
    return {
        "total": total,
        "currentPage": current_page,
        "pageSize": page_size,
        "totalPage": total_page,
        "records": records,
    }
