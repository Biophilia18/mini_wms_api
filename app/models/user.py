"""
@ coding : utf-8 
@Time    : 2025/10/25 09:20
@Author  : admin
@Project : fastapi_wms
@File    : user.py
@Software: PyCharm
@Notes   : 用户表模型
"""
from sqlalchemy import Column, String, Integer, Boolean

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
