"""
@ coding : utf-8 
@Time    : 2025/10/25 12:14
@Author  : admin
@Project : fastapi_wms
@File    : dependencies.py
@Software: PyCharm
@Notes   : 依赖注入定义
"""
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.database import get_db
from app.dao.user_dao import UserDAO
from app.schemas.user import UserInfo
from app.utils.jwt import verify_access_token

# 提供FastApi 依赖项，用于jwt令牌验证和用户验证

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
user_dao = UserDAO()

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效token")

        usr_id: int = payload.get("user_id")
        if usr_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="缺少用户信息")

        user = user_dao.get(db, usr_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在或已删除")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
