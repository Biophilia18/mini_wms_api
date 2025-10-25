"""
@ coding : utf-8 
@Time    : 2025/10/25 14:48
@Author  : admin
@Project : fastapi_wms
@File    : log_middleware.py
@Software: PyCharm
@Notes   :
"""
import time

from fastapi import Request
from jose import jwt
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import logger

# secret key 和算法
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # token有效期
SLOW_REQUEST_THRESHOLD_MS = 1000  # 1秒


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        user_id = "anonymous"
        # 从header中解析user_id（如有）
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer"):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = payload.get("user_id", "unknown")
            except Exception:
                user_id = "invalid_token"

        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000  # ms
        log_message = {
            f"{request.method} {request.url.path} | "
            f"User: {user_id} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time:.2f} ms"
        }
        # ✅ 成功和错误区分颜色等级
        if response.status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        if process_time > SLOW_REQUEST_THRESHOLD_MS:
            logger.warning(f"⚠️ Slow API Detected: {log_message}")

        return response
