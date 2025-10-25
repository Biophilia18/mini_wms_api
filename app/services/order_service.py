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


class OrderService:
    def __init__(self, db: Session):
        self.order_dao = OrderDAO()

    def create_order(self, db: Session, order_no: str, user_id: int):
        self.order_dao.create_order(db, order_no, user_id)
        return f"订单创建成功：{order_no}"

    def list_orders(self, db: Session):
        orders = self.order_dao.get_all_orders(db)
        return [f"{o.id}-{o.order_no}-{o.status}" for o in orders]

