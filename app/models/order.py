"""
@ coding : utf-8 
@Time    : 2025/10/25 09:23
@Author  : admin
@Project : fastapi_wms
@File    : order.py
@Software: PyCharm
@Notes   :订单表模型
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="created")

    # 关系映射
    user = relationship("User", backref="orders")
