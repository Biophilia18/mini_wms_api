"""
@ coding : utf-8 
@Time    : 2025/10/26 11:26
@Author  : admin
@Project : fastapi_wms
@File    : stock_log.py
@Software: PyCharm
@Notes   : stock_log 接口层
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.stock_log import StockLogInfo, StockLogCreate
from app.services.stock_log_service import StockLogService

rt_stock = APIRouter(prefix="/stock", tags=["stock_log"])
stock_service = StockLogService()

@rt_stock.post("/record", response_model=ResponseModel[StockLogInfo])
def record_stock_change(
        stock_in: StockLogCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """记录一次出入库操作"""
    log = stock_service.record_stock_change(db, stock_in, current_user.id)
    return ResponseModel(data=log)

@rt_stock.get("/inventory/{inventory_id}", response_model=ResponseModel[List[StockLogInfo]])
def list_logs_by_inventory(
        inventory_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """查询某库存记录的历史变动"""
    logs = stock_service.list_logs_by_inventory(db, inventory_id)
    return ResponseModel(data=logs)

