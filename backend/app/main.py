from fastapi import FastAPI

from app.setting.config import (
    register_middleware, 
    register_router, 
    register_exception_handler
)

def create_app()-> FastAPI:
    app = FastAPI(
        title="Campus Activity System API",
        middleware=register_middleware(),
    )

    register_router(app)
    register_exception_handler(app)
    
    return app

app = create_app()
