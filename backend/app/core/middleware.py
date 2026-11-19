import traceback
from datetime import datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.log.context import LogContext


class HttpMiddleware(BaseHTTPMiddleware):
    """请求日志中间件：注入 request_id 并记录请求开始/完成/异常"""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now()

        incoming_id = request.headers.get("x-request-id") or request.headers.get(
            "X-Request-ID"
        )
        request_id = LogContext.set_request_id(incoming_id)
        request.state.request_id = request_id
        LogContext.update_context(
            method=request.method,
            path=request.url.path,
            url=str(request.url),
            query_params=dict(request.query_params),
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        context_logger = LogContext.get_logger()
        context_logger.info(f"请求开始: {request.method} {request.url.path}")

        try:
            response = await call_next(request)
            process_time = (datetime.now() - start_time).total_seconds() * 1000

            response.headers["X-Request-ID"] = request_id
            LogContext.update_context(
                status_code=response.status_code,
                process_time_ms=round(process_time, 2),
            )
            context_logger.info(
                f"请求完成: {request.method} {request.url.path} - "
                f"{response.status_code} ({process_time:.2f}ms)"
            )
            return response

        except Exception as exc:
            process_time = (datetime.now() - start_time).total_seconds() * 1000
            LogContext.update_context(
                exception_occurred=True,
                exception_type=type(exc).__name__,
                exception_msg=str(exc),
                process_time_ms=round(process_time, 2),
                traceback=traceback.format_exc(),
            )
            context_logger.error(
                f"请求处理异常: {request.method} {request.url.path} - "
                f"{type(exc).__name__}: {exc} ({process_time:.2f}ms)"
            )
            raise

        finally:
            LogContext.clear()
