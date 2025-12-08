"""
@ coding : utf-8 
@Time    : 2025/10/25 10:33
@Author  : admin
@Project : fastapi_wms
@File    : base.py
@Software: PyCharm
@Notes   : 统一响应结构定义
"""
from typing import TypeVar, Generic, Optional

from pydantic import BaseModel
# 泛型 ，用于通用相应类型
T = TypeVar('T')
class ResponseModel(BaseModel, Generic[T]):
    """
    统一响应格式：
        code : 响应码（0表示成功，非0表示业务错误）
        message : 响应信息
        data : 实际数据内容（可为任意类型）
    """
    code: int=0
    message: str="success"
    data: Optional[T]=None

    model_config = {
        "from_attributes": True
    }

class ErrorCode:
    """
    业务错误码定义：
        PARAM_ERROR : 参数错误
        AUTH_ERROR : 权限错误
        DB_ERROR : 数据库错误
        UNKNOWN_ERROR : 未知错误
    """
    PARAM_ERROR = 1000
    AUTH_ERROR = 1001
    DB_ERROR = 1002
    UNKNOWN_ERROR = 1003
