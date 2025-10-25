"""
@ coding : utf-8 
@Time    : 2025/10/25 09:28
@Author  : admin
@Project : fastapi_wms
@File    : order_dao.py
@Software: PyCharm
@Notes   : 订单DAO层
"""
from sqlalchemy.orm import Session

from app.models.order import Order


class OrderDAO:
    def create_order(self, db: Session, order_no: str, user_id: int):
        order = Order(order_no=order_no, user_id=user_id)
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    def get_all_orders(self, db: Session):
        return db.query(Order).all()