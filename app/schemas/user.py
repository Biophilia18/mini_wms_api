"""
@ coding : utf-8 
@Time    : 2025/10/25 10:36
@Author  : admin
@Project : fastapi_wms
@File    : user.py
@Software: PyCharm
@Notes   : 用户相关数据模型（输入输出）
"""
from pydantic import BaseModel, EmailStr, Field


# 输入模型
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    password: str = Field(..., min_length=3, max_length=50, description="密码")
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

# 输出模型
class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True # 允许从ORM模型自动转换