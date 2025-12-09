"""
@ coding : utf-8
@Time    : 2025/12/09 23:55
@Author  : admin1
@Project : fastapi_wms
@File    : transfer.py
@Desc    :
@Notes   : 调拨模块 Pydantic 数据模型定义
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# ============================================================
# 调拨明细（TransferItem）相关模型
# ============================================================

class TransferItemCreate(BaseModel):
    """
    调拨明细创建入参模型：
      - 用于创建调拨单时前端提交的每一行商品调拨数据
      - 对应 transfer_items 表，不包含 id 等自动生成字段
    """
    product_id: int = Field(..., gt=0, description="商品ID，对应 products.id")
    quantity: int = Field(..., gt=0, description="调拨数量，必须为正整数")
    unit_price: Optional[float] = Field(
        default=None,
        gt=0,
        description="调拨单价（可选，用于成本核算或估值）"
    )
    remark: Optional[str] = Field(
        default=None,
        max_length=255,
        description="行备注信息，例如批次或特殊说明"
    )


class TransferItemInfo(BaseModel):
    """
    调拨明细响应模型：
      - 接口返回时展示调拨明细信息
      - 包含主键 id 字段，方便前端后续操作
    """
    id: int
    product_id: int
    quantity: int
    unit_price: Optional[float] = None
    remark: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


# ============================================================
# 调拨单（TransferOrder）相关模型
# ============================================================

class TransferOrderCreate(BaseModel):
    """
    调拨单创建入参模型：
      - 用于前端创建调拨单时提交的数据结构
      - 不包含 transfer_no（由后端生成）
      - 必须传入调出仓、调入仓及明细列表
    """
    source_warehouse_id: int = Field(..., gt=0, description="调出仓库ID，对应 warehouses.id")
    target_warehouse_id: int = Field(..., gt=0, description="调入仓库ID，对应 warehouses.id")
    remark: Optional[str] = Field(
        default=None,
        max_length=255,
        description="调拨单备注，例如调拨原因或说明"
    )
    items: List[TransferItemCreate] = Field(
        ...,
        description="调拨明细列表，至少包含一条明细记录"
    )


class TransferOrderUpdate(BaseModel):
    """
    调拨单状态更新模型：
      - 用于更新调拨单的状态（审批、执行、确认）
      - 状态限定为固定字符串值，防止非法传入
      - 状态流转：created → approved → executed → confirmed
    """
    status: str = Field(
        ...,
        pattern="^(created|approved|executed|confirmed)$",
        description="调拨单状态，只允许 created/approved/executed/confirmed 之一"
    )


class TransferOrderInfo(BaseModel):
    """
    调拨单响应模型：
      - 接口返回调拨单详情或列表时使用
      - 包含调出/调入仓库、状态、时间、明细列表等信息
    """
    id: int
    transfer_no: str
    source_warehouse_id: int
    target_warehouse_id: int
    status: str
    created_by: int
    remark: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[TransferItemInfo] = []

    model_config = {
        "from_attributes": True
    }
