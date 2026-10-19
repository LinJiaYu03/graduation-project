from pydantic import BaseModel,Field
from typing import Optional,TypeVar,Generic
from app.core.context import request_id_ctx

T=TypeVar("T")

class BaseResponse(BaseModel,Generic[T]):
    code:int=Field(0, description="状态码")
    msg:str=Field("success", description="状态描述")
    data:Optional[T]=Field(None, description="数据")
    request_id:Optional[str]=Field(default_factory=lambda: request_id_ctx.get(), description="请求id")

class PageResponse(BaseModel,Generic[T]):
    code:int=Field(0, description="状态码")
    msg:str=Field("success", description="状态描述")
    total:int=Field(0, description="总条数")
    data:Optional[T]=Field(None, description="列表")
    request_id:Optional[str]=Field(default_factory=lambda: request_id_ctx.get(), description="请求id")
    page:int=Field(1, description="当前页")
