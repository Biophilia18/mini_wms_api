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
from app.schemas.user import UserRegister, UserLogin, UserInfo

class AuthService:
    def __init__(self):
        self.user_dao = UserDAO()

    def register(self, db: Session,user_in: UserRegister)-> UserInfo:
        # 检查用户名是否重复
        if self.user_dao.get_by_username(db, user_in.username):
            raise HTTPException(status_code=400, detail="用户名已存在")
        user_data = user_in.model_dump()
        new_user = self.user_dao.create(db, user_data)
        return new_user

    def login(self, db: Session, login_in: UserLogin)-> str:
        user = self.user_dao.get_by_username(db, login_in.username)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        if user.password != login_in.password:
            raise HTTPException(status_code=401, detail="密码错误")
        return f"登录成功,欢迎 {user.username}"
