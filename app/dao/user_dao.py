"""
@ coding : utf-8 
@Time    : 2025/10/25 09:26
@Author  : admin
@Project : fastapi_wms
@File    : user_dao.py
@Software: PyCharm
@Notes   : 用户dao层
    继承 BaseDAO，获得通用 CRUD 能力
    并可自定义额外查询方法（例如按用户名或邮箱）
"""
from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.user import User


class UserDAO(BaseDAO[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, db: Session, username: str):
        """根据用户名查询用户"""
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str):
        """根据邮箱查询用户"""
        return db.query(User).filter(User.email == email).first()
