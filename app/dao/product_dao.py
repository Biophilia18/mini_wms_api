"""
@ coding : utf-8 
@Time    : 2025/10/25 15:41
@Author  : admin
@Project : fastapi_wms
@File    : product_dao.py
@Software: PyCharm
@Notes   : 商品数据访问对象
"""
from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.product import Product


class ProductDAO(BaseDAO[Product]):
    def __init__(self):
        super().__init__(Product)

    def get_by_name(self, db:Session, name:str):
        """按商品名查询"""
        return db.query(Product).filter(Product.name==name).first()

    def get_by_sku(self, db:Session, sku:str):
        """按商品sku查询"""
        return db.query(Product).filter(Product.sku==sku).first()

