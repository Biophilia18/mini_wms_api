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
from app.services.auth_service import AuthService

rt_auth = APIRouter(prefix="/auth", tags=["auth,用户接口"])
auth_service = AuthService()

@rt_auth.post("/register")
def register(username:str, email:str, password:str, db:Session=Depends(get_db)):
    return {"msg": auth_service.register(db, username, email, password)}

@rt_auth.post("/login")
def login(username:str, password:str, db:Session=Depends(get_db)):
    return {"msg": auth_service.login(db, username, password)}