"""
@ coding : utf-8 
@Time    : 2025/10/26 11:05
@Author  : admin
@Project : fastapi_wms
@File    : stock_log.py
@Software: PyCharm
@Notes   : 出入库接口数据模型
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.stock_log import StockAction


class StockLogCreate(BaseModel):
    inventory_id: int = Field(..., gt=0, description="库存记录id")
    action: StockAction = Field(..., description="操作类型：in/out/adjust")
    change_qty: int = Field(..., description="变动数量（入库为正，出库为负")
    remark: Optional[str] = Field(None, description="备注")

class StockLogInfo(BaseModel):
    id: int
    inventory_id: int
    user_id: int
    action: StockAction
    change_qty: int
    remark: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }