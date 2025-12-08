"""
@ coding : utf-8 
@Time    : 2025/12/8 20:46
@Author  : admin1
@Project : fastapi_wms
@File    : inbound.py
@Desc    :
@Notes   :  入库模块数据模型定义
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# 入库明细(item)模型
class InboundItemCreate(BaseModel):
    """入库单明细创建结构"""
    product_id: int = Field(..., gt=0, description="商品id")
    quantity: int= Field(...,gt=0,description="入库数量")
    unit_price: Optional[float] = Field(None, gt=0,description="入库单价")
    remark: Optional[str] = Field(None,max_length=255, description="行备注")

class InboundItemInfo(BaseModel):
    """入库单明细响应结构"""
    id: int
    product_id: int
    quantity: int
    unit_price: Optional[float] = None
    remark: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# 入库单(order)模型
class InboundOrderCreate(BaseModel):
    """入库单创建结构"""
    warehouse_id: int = Field(..., gt=0, description="入库仓库id")
    supplier: Optional[str] = Field(None,max_length=100,description="供应商名称")
    items: List[InboundItemCreate] = Field(...,description="入库明细列表")

class InboundOrderUpdate(BaseModel):
    """入库单状态更新"""
    status: str = Field(..., pattern="^(created|approved|executed|confirmed)$", description="单据状态")

class InboundOrderInfo(BaseModel):
    """入库单响应结构"""
    id: int
    order_no: str
    warehouse_id: int
    supplier: Optional[str]
    status: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    items: List[InboundItemInfo] = []

    model_config = {
        "from_attributes": True
    }