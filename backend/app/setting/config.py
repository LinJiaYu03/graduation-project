from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from app.core.middleware import HttpMiddleware

from app.api import api_router
from app.core.exceptions import BizException
from fastapi.exceptions import RequestValidationError

from app.core.exceptions import (
    biz_handler,
    value_error_handler, 
    unhandled_exception_handler, 
    validation_exception_handler
)

# 注册中间件
def register_middleware():
   middleware = [
       Middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_methods=["*"],
       allow_headers=["*"],
    ),
    Middleware(HttpMiddleware)
    ]

   return middleware

# 注册路由
def register_router(app: FastAPI):
    app.include_router(api_router, prefix="/api")

# 注册异常处理函数
def register_exception_handler(app: FastAPI):
    app.add_exception_handler(BizException, biz_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)