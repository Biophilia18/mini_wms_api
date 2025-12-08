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
    """
    用户注册请求体：
        username : 用户名，长度3~20。
        password : 密码，长度3~50。
        email : 邮箱地址。
    """
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    password: str = Field(..., min_length=3, max_length=50, description="密码")
    email: EmailStr

class UserLogin(BaseModel):
    """
    用户登录请求体：
        username : 用户名。
        password : 密码。
    """
    username: str
    password: str

# 输出模型
class UserInfo(BaseModel):
    """
    用户信息响应体：
        id : 用户ID。
        username : 用户名。
        email : 邮箱。
        is_active : 是否启用。
    """
    id: int
    username: str
    email: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }#  允许从ORM模型自动转换
