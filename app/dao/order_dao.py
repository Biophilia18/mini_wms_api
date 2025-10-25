"""
@ coding : utf-8 
@Time    : 2025/10/25 09:28
@Author  : admin
@Project : fastapi_wms
@File    : order_dao.py
@Software: PyCharm
@Notes   : 订单DAO层
继承 BaseDAO，获得通用 CRUD 功能
"""
from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.order import Order


class OrderDAO(BaseDAO[Order]):
    def __init__(self):
        super().__init__(Order)
