"""
@ coding : utf-8 
@Time    : 2025/10/25 09:26
@Author  : admin
@Project : fastapi_wms
@File    : user_dao.py
@Software: PyCharm
@Notes   : 用户dao层，增删改查操作
"""
from sqlalchemy.orm import Session

from app.models.user import User


class UserDAO:
    def create_user(self, db: Session, username: str, email: str, password: str):
        user = User(username=username, email=email, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_all(self, db: Session):
        return db.query(User).all()
