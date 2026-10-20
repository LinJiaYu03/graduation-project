from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.context import set_request_id

class HttpMiddleware(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        incoming_id = request.headers.get("x-request-id") or request.headers.get(
            "X-Request-ID"
        )
        request_id=set_request_id(incoming_id)
        request.state.request_id=request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
