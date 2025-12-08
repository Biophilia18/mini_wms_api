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
    """
    创建出入库日志请求体：
        inventory_id : 库存记录ID。
        action : 操作类型（IN/OUT/ADJUST）。
        change_qty : 变动数量（入库为正，出库为负）。
        remark : 操作备注（可选）。
    """
    inventory_id: int = Field(..., gt=0, description="库存记录id")
    action: StockAction = Field(..., description="操作类型：in/out/adjust")
    change_qty: int = Field(..., description="变动数量（入库为正，出库为负")
    remark: Optional[str] = Field(None, description="备注")

class StockLogInfo(BaseModel):
    """
    出入库日志响应体：
        id : 日志ID。
        inventory_id : 库存记录ID。
        user_id : 操作用户ID。
        action : 操作类型（IN/OUT/ADJUST）。
        change_qty : 变动数量。
        remark : 备注信息。
        created_at : 创建时间。
    """
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
