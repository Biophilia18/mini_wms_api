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
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.user import UserInfo, UserRegister, UserLogin
from app.services.auth_service import AuthService
from app.utils.jwt import create_access_token

rt_auth = APIRouter(prefix="/auth", tags=["auth,用户接口"])
auth_service = AuthService()

@rt_auth.post("/register", response_model=ResponseModel[UserInfo])
def register(user_in: UserRegister, db:Session=Depends(get_db)):
    new_user = auth_service.register(db, user_in)
    return ResponseModel(data=new_user)

@rt_auth.post("/login", response_model=ResponseModel[dict])
def login(login_in: UserLogin, db:Session=Depends(get_db)):
    token_info = auth_service.login(db,login_in)
    return ResponseModel(data=token_info)

@rt_auth.get("/me", response_model=ResponseModel[UserInfo])
def get_me(current_user=Depends(get_current_user)):
    return ResponseModel(data=current_user)
