import traceback
from typing import Any

from fastapi import HTTPException, Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.response import error_response
from app.log import logger

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

def _request_log_extra(request: Request) -> dict:
    """异常日志通用的请求上下文信息"""
    return {
        "request_id": getattr(request.state, "request_id", "-"),
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host if request.client else None,
    }


def handle_exception(app: FastAPI) -> None:
    @app.exception_handler(BizException)
    async def biz_handler(request: Request, exc: BizException) -> JSONResponse:
        log = logger.bind(**_request_log_extra(request), code=exc.code)
        message = f"业务异常: {request.method} {request.url.path} - {exc.code}: {exc.msg}"
        if exc.code >= 500:
            log.error(message)
        else:
            log.warning(message)
        return JSONResponse(
            status_code=200,
            content=error_response(code=exc.code, message=exc.msg, data=exc.data),
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        logger.bind(**_request_log_extra(request)).warning(
            f"值异常: {request.method} {request.url.path} - {exc}"
        )
        return JSONResponse(
            status_code=200,
            content=error_response(code=400, message=str(exc)),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = []
        for err in exc.errors():
            errors.append(
                {"field": ".".join(str(x) for x in err["loc"]), "message": err["msg"]}
            )
        logger.bind(**_request_log_extra(request), validation_errors=errors).warning(
            f"参数校验失败: {request.method} {request.url.path} - {len(errors)}个错误"
        )
        return JSONResponse(
            status_code=200,
            content=error_response(code=400, message="参数校验失败", data={"errors": errors}),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.bind(
            **_request_log_extra(request),
            exception_type=type(exc).__name__,
            exception_msg=str(exc),
            traceback=traceback.format_exc(),
        ).critical(
            f"未处理的异常: {request.method} {request.url.path} - {type(exc).__name__}: {exc}"
        )
        return JSONResponse(
            status_code=200,
            content=error_response(code=400, message="服务器内部错误: " + str(exc)),
        )
