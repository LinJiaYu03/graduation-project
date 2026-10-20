from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api.user import user_router
from app.api.campus import campus_router
from app.api.club import club_router
from app.api.activity import activity_router
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

app.include_router(user_router)
app.include_router(campus_router)
app.include_router(club_router)
app.include_router(activity_router)


@app.exception_handler(BizException)
async def biz_handler(request: Request, exc: BizException):
    return JSONResponse(
        status_code=200,
        content=error_response(code=exc.code, message=exc.msg, data=exc.data),
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
