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
    """
    用户数据访问层：
        封装对用户表的基础操作（查询、创建、更新、删除）。
        所有数据库会话在 Service 层统一管理。
    """
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, db: Session, username: str) -> User | None:
        """
        根据用户名查询用户
        :param db: 数据库会话
        :param username: 用户名
        :return: 匹配的用户对象，若不存在返回 None
        """
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str):
        """根据邮箱查询用户"""
        return db.query(User).filter(User.email == email).first()
