from fastapi import FastAPI

from app import (
    register_middleware, 
    register_router, 
    register_exception_handler
)
from app.log import logger

def create_app()-> FastAPI:
    app = FastAPI(
        title="Campus Activity System API",
        middleware=register_middleware(),
    )

    register_router(app)
    register_exception_handler(app)
    
    return app

app = create_app()
logger.bind(event="app_startup").info("Campus Activity System API 应用已创建")

