"""
@ coding : utf-8 
@Time    : 2025/10/26 11:12
@Author  : admin
@Project : fastapi_wms
@File    : stock_log_service.py
@Software: PyCharm
@Notes   : 出入库业务逻辑
"""
from sqlalchemy.orm import Session

from app.dao.inventory_dao import InventoryDAO
from app.dao.stock_log_dao import StockLogDAO
from app.middleware.exceptions import AppException
from app.schemas.base import ErrorCode
from app.schemas.stock_log import StockLogCreate


class StockLogService:
    def __init__(self):
        self.stock_dao = StockLogDAO()
        self.inventory_dao = InventoryDAO()

    def record_stock_change(self,db:Session, stock_in: StockLogCreate, user_id: int):
        """记录一次库存变动，并更新库存数量"""
        inv = self.inventory_dao.get(db,stock_in.inventory_id)
        if not inv:
            raise AppException(ErrorCode.PARAM_ERROR,"库存记录不存在")
        # 更新库存
        new_qty = inv.quantity + stock_in.change_qty
        if new_qty <0:
            raise AppException(ErrorCode.PARAM_ERROR,"库存不足，无法出库")
        # 写入日志
        inv.quantity = new_qty
        db.commit()
        db.refresh(inv)

        new_log = self.stock_dao.create(db,{
            "inventory_id":stock_in.inventory_id,
            "user_id":user_id,
            "action":stock_in.action,
            "change_qty":stock_in.change_qty,
            "remark":stock_in.remark
        })
        return new_log

    def list_logs_by_inventory(self, db:Session, inventory_id: int):
        """查询某库存的变动记录"""
        return self.stock_dao.list_by_inventory(db,inventory_id)