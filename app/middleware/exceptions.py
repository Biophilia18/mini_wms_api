"""
@ coding : utf-8 
@Time    : 2025/10/25 14:15
@Author  : admin
@Project : fastapi_wms
@File    : exceptions.py
@Software: PyCharm
@Notes   :
"""
from fastapi import HTTPException, status

class AppException(HTTPException):
    """统一业务异常类"""
    def __init__(self, code: int, message: str):
        super().__init__(status_code=status.HTTP_200_OK, detail={"code": code, "message":message})