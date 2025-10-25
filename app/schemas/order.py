"""
@ coding : utf-8 
@Time    : 2025/10/25 10:39
@Author  : admin
@Project : fastapi_wms
@File    : order.py
@Software: PyCharm
@Notes   : 订单相关数据模型
"""
from pydantic import BaseModel, Field

class OrderCreate(BaseModel):
    order_no: str = Field(..., min_length=5, max_length=30, description="订单号")
    user_id: int = Field(..., gt=0, description="下单用户id")

class OrderInfo(BaseModel):
    id: int
    order_no: str
    user_id: int
    status: str

    class Config:
        orm_mode = True