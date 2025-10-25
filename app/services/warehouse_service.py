"""
@ coding : utf-8 
@Time    : 2025/10/25 17:31
@Author  : admin
@Project : fastapi_wms
@File    : warehouse_service.py
@Software: PyCharm
@Notes   : 仓库业务逻辑
"""
from sqlalchemy.orm import Session
from app.dao.warehouse_dao import WareHouseDAO
from app.middleware.exceptions import AppException
from app.schemas.base import ErrorCode
from app.schemas.warehouse import WarehouseCreate


class WareHouseService:
    def __init__(self):
        self.warehouse_dao = WareHouseDAO()

    def create_warehouse(self, db: Session, warehouse_in: WarehouseCreate):
        """创建新仓库"""
        if self.warehouse_dao.get_by_code(db, warehouse_in.code):
            raise AppException(ErrorCode.PARAM_ERROR, "仓库编码已存在")
        if self.warehouse_dao.get_by_name(db, warehouse_in.name):
            raise AppException(ErrorCode.PARAM_ERROR, "仓库名称已存在")
        new_warehouse = self.warehouse_dao.create(db, warehouse_in.model_dump())
        return new_warehouse

    def list_warehouses(self, db:Session):
        """获取仓库列表"""
        return self.warehouse_dao.get_active_warehouses(db)

    def toggle_warehouse_status(self, db: Session, warehouse_id: int):
        """切换仓库启用、禁用状态"""
        warehouse = self.warehouse_dao.get(db, warehouse_id)
        if not warehouse:
            raise AppException(ErrorCode.PARAM_ERROR, "仓库不存在")
        warehouse.is_active = not warehouse.is_active
        db.commit()
        db.refresh(warehouse)
        return warehouse
