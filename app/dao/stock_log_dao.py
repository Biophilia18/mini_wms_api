"""
@ coding : utf-8 
@Time    : 2025/10/26 11:09
@Author  : admin
@Project : fastapi_wms
@File    : stock_log_dao.py
@Software: PyCharm
@Notes   : 出入库记录DAO层
"""
from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.stock_log import StockLog


class StockLogDAO(BaseDAO[StockLog]):
    def __init__(self):
        super().__init__(StockLog)

    def list_by_inventory(self,db: Session, inventory_id: int):
        """查询某库存的所有变动记录"""
        return db.query(StockLog).filter(StockLog.inventory_id == inventory_id).all()

    def list_by_user(self,db: Session, user_id: int):
        """查询某用户的操作日志"""
        return db.query(StockLog).filter(StockLog.user_id == user_id).all()
