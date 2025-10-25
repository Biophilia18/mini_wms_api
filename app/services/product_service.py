"""
@ coding : utf-8 
@Time    : 2025/10/25 15:44
@Author  : admin
@Project : fastapi_wms
@File    : product_service.py
@Software: PyCharm
@Notes   : 商品业务逻辑层
"""
from sqlalchemy.orm import Session

from app.dao.product_dao import ProductDAO
from app.middleware.exceptions import AppException
from app.schemas.base import ErrorCode
from app.schemas.product import ProductCreate


class ProductService:
    def __init__(self):
        self.product_dao = ProductDAO()

    def create_product(self, db:Session, product_in: ProductCreate):
        """创建新商品"""
        if self.product_dao.get_by_name(db, product_in.name):
            raise AppException(ErrorCode.PARAM_ERROR,"商品名称已存在")
        if self.product_dao.get_by_sku(db, product_in.sku):
            raise AppException(ErrorCode.PARAM_ERROR, "SKU已存在")
        new_product = self.product_dao.create(db, product_in.model_dump())
        return new_product

    def list_products(self, db:Session):
        """查询全部商品"""
        return self.product_dao.get_all(db)