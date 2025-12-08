"""
@ coding : utf-8 
@Time    : 2025/10/25 09:40
@Author  : admin
@Project : fastapi_wms
@File    : auth.py
@Software: PyCharm
@Notes   : controller层，用户模块路由
"""
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.user import UserInfo, UserRegister, UserLogin
from app.services.auth_service import AuthService

rt_auth = APIRouter(prefix="/auth", tags=["auth,用户接口"])
auth_service = AuthService()

@rt_auth.post("/register", response_model=ResponseModel[UserInfo])
def register(user_in: UserRegister, db:Session=Depends(get_db)):
    """
    用户注册接口
    :param user_in:
        user_in.username : 用户名，唯一
        user_in.password : 登录密码
        user_in.email : 用户邮箱
    :param db: 数据库会话
    :return: 用户基本信息（id、username、email、is_active）
    """
    new_user = auth_service.register(db, user_in)
    return ResponseModel(data=new_user)

@rt_auth.post("/login", response_model=ResponseModel[dict])
def login(login_in: UserLogin, db:Session=Depends(get_db)):
    """
    用户登录
    :param login_in:
        ogin_in.username : 用户名
        login_in.password : 登录密码
    :param db: 数据库会话
    :return:
        access_token : 访问令牌
        token_type : 令牌类型
        expires : 过期时间
    """
    token_info = auth_service.login(db,login_in)
    return ResponseModel(data=token_info)

@rt_auth.get("/me", response_model=ResponseModel[UserInfo])
def get_me(current_user=Depends(get_current_user)):
    """
    获取当前登录用户信息
    :param current_user: 当前登录用户，从token解析
    :return: 用户基本信息
    """
    return ResponseModel(data=current_user)
