from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from app.core.middleware import HttpMiddleware

from app.api import api_router
from app.core.exceptions import handle_exception

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
    handle_exception(app)
