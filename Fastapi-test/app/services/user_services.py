from sqlalchemy.orm import Session
from app.models.user import User
from app.core.respones import success_response
from app.core.exceptions import BizException

def get_user(db:Session, id:int):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise BizException(code=404, msg="用户不存在")
    return success_response(data=user,msg="获取用户成功")

def get_users(db:Session, page:int=1, page_size:int=10):
    total=db.query(User).count()
    users=db.query(User).offset((page-1)*page_size).limit(page_size).all()
    
    return success_response(
        data=users,
        total=total,
        page=page,
        page_size=page_size,
        msg="获取用户列表成功"
    )

def create_user(db:Session, user:User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

