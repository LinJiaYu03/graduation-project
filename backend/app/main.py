from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.middleware import HttpMiddleware
from app.core.respones import error_response
from app.core.exceptions import BizException

app = FastAPI(title="Campus Activity System API")

app.add_middleware(HttpMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api")


@app.exception_handler(BizException)
async def biz_handler(request: Request, exc: BizException):
    return JSONResponse(
        status_code=200,
        content=error_response(code=exc.code, message=exc.msg, data=exc.data),
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=200,
        content=error_response(code=400, message=str(exc)),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content=error_response(code=400, message="服务器内部错误: " + str(exc)),
    )


@app.exception_handler(RequestValidationError)
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
