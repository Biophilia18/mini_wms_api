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
    """
    创建订单请求体：
        order_no : 订单编号（唯一，长度5~30）。
        user_id : 下单用户ID。
    """
    order_no: str = Field(..., min_length=5, max_length=30, description="订单号")
    user_id: int = Field(..., gt=0, description="下单用户id")

class OrderInfo(BaseModel):
    """
    订单信息响应体：
        id : 订单ID。
        order_no : 订单编号。
        user_id : 用户ID。
        status : 订单状态。
    """
    id: int
    order_no: str
    user_id: int
    status: str

    model_config = {
        "from_attributes": True
    }
