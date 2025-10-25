"""
@ coding : utf-8 
@Time    : 2025/10/25 09:31
@Author  : admin
@Project : fastapi_wms
@File    : auth_service.py
@Software: PyCharm
@Notes   : 认证业务逻辑
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dao.user_dao import UserDAO


class AuthService:
    def __init__(self):
        self.user_dao = UserDAO()

    def register(self, db: Session, username: str, email: str, password: str):
        if self.user_dao.get_user_by_username(db, username):
            raise HTTPException(status_code=400, detail="用户名已存在")
        self.user_dao.create_user(db, username, email, password)
        return f"注册成功, {username} is active"

    def login(self, db: Session, username: str, password: str):
        user = self.user_dao.get_user_by_username(db, username)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        if user.password != password:
            raise HTTPException(status_code=401, detail="密码错误")
        return f"登录成功,欢迎 {username}"
