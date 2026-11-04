from typing import Any, Generic, TypeVar
import math

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一响应结构"""

    code: int = 200
    message: str = "操作成功"
    success: bool = True
    data: T | None = None


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
