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
    """统一响应格式"""
    code: int=0
    message: str="success"
    data: Optional[T]=None
