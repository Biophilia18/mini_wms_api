"""
@ coding : utf-8 
@Time    : 2025/10/26 09:44
@Author  : admin
@Project : fastapi_wms
@File    : inventory_service.py
@Software: PyCharm
@Notes   : 库存业务逻辑层（service）
"""
from sqlalchemy.orm import Session

from app.dao.inventory_dao import InventoryDAO
from app.middleware.exceptions import AppException
from app.schemas.base import ErrorCode
from app.schemas.inventory import InventoryCreate, InventoryUpdate


class InventoryService:
    def __init__(self):
        self.inventory_dao = InventoryDAO()

    def create_inventory(self, db: Session, inv_in: InventoryCreate):
        """创建库存记录，商品+仓库唯一"""
        exist = self.inventory_dao.get_by_product_warehouse(db, inv_in.product_id, inv_in.warehouse_id)
        if exist:
            raise AppException(ErrorCode.PARAM_ERROR, "该商品在仓库的库存记录已存在")
        return self.inventory_dao.create(db, inv_in.model_dump())

    def update_quantity(self, db: Session, inv_id: int, inv_update: InventoryUpdate):
        """更新库存数量"""
        inv = self.inventory_dao.get(db, inv_id)
        if not inv:
            raise AppException(ErrorCode.PARAM_ERROR, "库存记录不存在")
        inv.quantity = inv_update.quantity
        db.commit()
        db.refresh(inv)
        return inv

    def list_by_product(self, db: Session, product_id: int):
        """查询某商品的所有库存"""
        return self.inventory_dao.list_by_product(db, product_id)

    def list_by_warehouse(self, db: Session, warehouse_id: int):
        """查询某仓库的所有库存"""
        return self.inventory_dao.list_by_warehouse(db, warehouse_id)
