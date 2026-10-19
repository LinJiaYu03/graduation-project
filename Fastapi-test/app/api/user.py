from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserResponse
from app.services.user_services import get_user,create_user,get_users
from app.schemas.user import UserCreate
from app.models.user import User
from app.schemas.response import BaseResponse,PageResponse

user_router=APIRouter()

@user_router.get("/user/{id}",response_model=BaseResponse[UserResponse])
def get_user_detail(id:int,db:Session=Depends(get_db)):
    user=get_user(db,id)
    return user

@user_router.post("/user",response_model=UserResponse)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    db_user=User(**user.model_dump())
    user=create_user(db,db_user)
    return user

@user_router.get("/users",response_model=PageResponse[list[UserResponse]])
def get_user_list(page:int=1,page_size:int=10,db:Session=Depends(get_db)):
    users=get_users(db,page,page_size)
    return users
