"""
@ coding : utf-8 
@Time    : 2025/10/25 09:17
@Author  : admin
@Project : fastapi_wms
@File    : database.py
@Software: PyCharm
@Notes   :
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 数据库链接信息
# DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/flask_demo"
DATABASE_URL = "mysql+pymysql://root:123456@111.228.4.79:3307/wmsmini"
# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)
# 创建Session工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# ORM基类
Base = declarative_base()
# fastapi依赖项，每次请求创建一个Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

