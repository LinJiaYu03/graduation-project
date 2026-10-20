from fastapi import HTTPException
from typing import Any

class BizException(HTTPException):
    def __init__(
            self, 
            code: int, 
            msg: str,
            data:Any|None=None
        )->None:
        super().__init__(status_code=code, detail=msg)
        self.code = code
        self.msg = msg
        self.data = data
