"""
@ coding : utf-8 
@Time    : 2025/10/25 09:20
@Author  : admin
@Project : fastapi_wms
@File    : product.py
@Software: PyCharm
@Notes   : 产品表模型
"""
from sqlalchemy import Column, String, Integer, Boolean, Float

from app.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
