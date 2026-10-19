from contextvars import ContextVar
import uuid

request_id_ctx: ContextVar[ str | None ] = ContextVar("request_id",default= None)

def set_request_id(request_id: str) -> str|None:
    if not request_id:
        request_id = str(uuid.uuid4())
    request_id_ctx.set(request_id)
    return request_id

