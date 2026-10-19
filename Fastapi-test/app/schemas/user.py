from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

# 创建用户请求模型
class UserCreate(BaseModel):
    username:str=Field(..., description="用户名")
    password:str=Field(..., description="密码")
    age:Optional[int]=Field(None, description="年龄")

# 用户响应模型
class UserResponse(BaseModel):
    id:int=Field(..., description="用户id")
    username:str=Field(..., description="用户名")
    password:str=Field(..., description="密码")
    age:Optional[int]=Field(None, description="年龄")
    create_time:datetime=Field(..., description="创建时间")
    update_time:datetime=Field(..., description="更新时间")

    class Config:
        from_attributes=True

# 更新用户请求模型
class UserUpdate(BaseModel):
    username:str=Field(None, description="用户名")
    password:str=Field(None, description="密码")
    age:Optional[int]=Field(None, description="年龄")
