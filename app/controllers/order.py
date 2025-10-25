"""
@ coding : utf-8 
@Time    : 2025/10/25 09:45
@Author  : admin
@Project : fastapi_wms
@File    : order.py
@Software: PyCharm
@Notes   : 订单路由
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.base import ResponseModel
from app.schemas.order import OrderInfo, OrderCreate
from app.services.order_service import OrderService

rt_order = APIRouter(prefix="/order", tags=["order，订单路由接口"])
order_service = OrderService()

@rt_order.post("/create", response_model=ResponseModel[OrderInfo])
def create_order(order_in: OrderCreate, db: Session=Depends(get_db)):
    new_order = order_service.create_order(db, order_in)
    return ResponseModel(data=new_order)

@rt_order.post("/list", response_model=ResponseModel[List[OrderInfo]])
def list_orders(db: Session=Depends(get_db)):
    orders = order_service.list_orders(db)
    return ResponseModel(data=orders)
