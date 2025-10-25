"""
@ coding : utf-8 
@Time    : 2025/10/25 09:37
@Author  : admin
@Project : fastapi_wms
@File    : order_service.py
@Software: PyCharm
@Notes   :
"""
from sqlalchemy.orm import Session

from app.dao.order_dao import OrderDAO
from app.schemas.order import OrderCreate


class OrderService:
    def __init__(self):
        self.order_dao = OrderDAO()

    def create_order(self, db: Session, order_in: OrderCreate):
        order_data = order_in.model_dump()
        new_order = self.order_dao.create(db, order_data)
        return new_order

    def list_orders(self, db: Session):
        return self.order_dao.get_all(db)

