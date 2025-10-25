"""
@ coding : utf-8 
@Time    : 2025/10/25 14:17
@Author  : admin
@Project : fastapi_wms
@File    : exception_middleware.py
@Software: PyCharm
@Notes   : 全局异常处理中间件
"""
import traceback

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from app.middleware.exceptions import AppException
from app.schemas.base import ResponseModel, ErrorCode


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except AppException as e:
            # 捕获业务异常
            return JSONResponse(
                status_code=200,
                content=ResponseModel(code=e.detail["code"], message=e.detail["message"], data=None).model_dump()
            )
        except Exception as e:
            # 捕获未知异常
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content=ResponseModel(code=ErrorCode.UNKNOWN_ERROR, message=str(e), data=None).model_dump()
            )
