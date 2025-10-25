"""
@ coding : utf-8 
@Time    : 2025/10/25 09:13
@Author  : admin
@Project : fastapi_wms
@File    : main.py
@Software: PyCharm
@Notes   :
"""
import uvicorn
from fastapi import FastAPI
from app.database import Base, engine
from app.controllers import auth, order, product
from app.middleware.log_middleware import LoggingMiddleware
from app.middleware.exception_middleware import ExceptionMiddleware

# 创建数据库表
Base.metadata.create_all(bind=engine)
# 实例化app
app = FastAPI(title="FastAPI-WMS", description="WMS API")
# 注册中间件
app.add_middleware(LoggingMiddleware)
app.add_middleware(ExceptionMiddleware)


# 注册路由
app.include_router(auth.rt_auth)
app.include_router(order.rt_order)
app.include_router(product.rt_product)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5050, reload=True)