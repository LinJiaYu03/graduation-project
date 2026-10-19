from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库url
SQLALCHEMY_DATABASE_URL ="mysql+pymysql://root:123456@localhost:3306/test"
# 数据库引擎
engine=create_engine(SQLALCHEMY_DATABASE_URL)
# 数据库会话
SessionLocal =sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
# 数据库模型基类
Base=declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()