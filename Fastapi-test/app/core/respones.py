from typing import Any

def success_response(
        code:int=0,
        data:Any|None=None,
        msg:str='success',
        **kwargs
        )->dict:
        
    return {
        "code":code,
        "data":data,
        "msg":msg,
        **kwargs,
    }

def error_response(
        code:int,
        data:Any|None=None,
        msg:str='error',
        )->dict:
    return {
        "code":code,
        "data":data,
        "msg":msg, 
    }
