from fastapi import HTTPException, Request
from typing import Any
from fastapi.responses import JSONResponse
from app.core.respones import error_response
from fastapi.exceptions import RequestValidationError

class BizException(HTTPException):
    def __init__(
            self, 
            code: int, 
            msg: str,
            data:Any|None=None
        )->None:
        super().__init__(status_code=code, detail=msg)
        self.code = code
        self.msg = msg
        self.data = data

async def biz_handler(request: Request, exc: BizException):
    return JSONResponse(
        status_code=200,
        content=error_response(code=exc.code, message=exc.msg, data=exc.data),
    )

async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=200,
        content=error_response(code=400, message=str(exc)),
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content=error_response(code=400, message="服务器内部错误: " + str(exc)),
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append(
            {"field": ".".join(str(x) for x in err["loc"]), "message": err["msg"]}
        )
    return JSONResponse(
        status_code=200,
        content=error_response(code=400, message="参数校验失败", data={"errors": errors}),
    )
