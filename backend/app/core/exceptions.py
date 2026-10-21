from fastapi import HTTPException, Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from typing import Any

from app.core.respones import error_response

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

def handle_exception(app: FastAPI) -> None:
    @app.exception_handler(BizException)
    async def biz_handler(request: Request, exc: BizException) -> JSONResponse:
        return JSONResponse(
            status_code=200,
            content=error_response(code=exc.code, message=exc.msg, data=exc.data),
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
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
        return JSONResponse(
            status_code=200,
            content=error_response(code=400, message="参数校验失败", data={"errors": errors}),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=200,
            content=error_response(code=400, message="服务器内部错误: " + str(exc)),
        )
