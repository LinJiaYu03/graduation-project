from fastapi import FastAPI
from app.api.user import user_router
from app.db.database import Base, engine
from app.core.middleware import HttpMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.respones import error_response
from app.core.exceptions import BizException

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
app.add_middleware(HttpMiddleware)


@app.exception_handler(BizException)
async def biz_handler(request: Request, exc: BizException):
    return JSONResponse(
        status_code=200,
        content=error_response(code=exc.code, msg=exc.msg, data=exc.data)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in err["loc"]),
            "message": err["msg"],
        })
    return JSONResponse(
        status_code=200,
        content=error_response(1001, "参数校验失败", {"errors": errors})
    )

