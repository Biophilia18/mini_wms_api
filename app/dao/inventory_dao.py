"""
@ coding : utf-8 
@Time    : 2025/10/26 09:31
@Author  : admin
@Project : fastapi_wms
@File    : inventory_dao.py
@Software: PyCharm
@Notes   : 库存数据访问层
"""
from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.inventory import Inventory


class InventoryDAO(BaseDAO[Inventory]):
    def __init__(self):
        super().__init__(Inventory)

    def get_by_product_warehouse(self, db: Session, product_id: int, warehouse_id: int):
        """根据商品和仓库id联合查询库存"""
        return (
            db.query(Inventory).filter(
                Inventory.product_id == product_id,
                Inventory.warehouse_id == warehouse_id
            ).first()
        )

    def list_by_product(self, db: Session, product_id: int):
        """查询某商品的所有仓库库存"""
        return db.query(Inventory).filter(Inventory.product_id == product_id).all()

    def list_by_warehouse(self, db: Session, warehouse_id: int):
        """查询某仓库的所有商品库存"""
        return db.query(Inventory).filter(Inventory.warehouse_id == warehouse_id).all()
