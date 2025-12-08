"""
@ coding : utf-8 
@Time    : 2025/12/8 22:38
@Author  : admin1
@Project : fastapi_wms
@File    : outbound_service.py
@Desc    :
@Notes   : 出库模块 Pydantic 数据模型定义
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ============================================================
# 出库明细（OutboundItem）相关模型
# ============================================================

class OutboundItemCreate(BaseModel):
    """
    出库明细创建入参模型：
      - 用于创建出库单时，前端提交的每一行商品出库数据
      - 对应数据库中的 outbound_items 表，但不包含 id 等数据库自动生成字段
    """
    product_id: int = Field(..., gt=0, description="商品ID，对应 products.id")
    quantity: int = Field(..., gt=0, description="出库数量，必须为正整数")
    unit_price: Optional[float] = Field(
        default=None,
        gt=0,
        description="出库单价（含税），可选字段，不传则认为不关心价格"
    )
    remark: Optional[str] = Field(
        default=None,
        max_length=255,
        description="行备注，例如特殊说明、批次、拣货要求等"
    )


class OutboundItemInfo(BaseModel):
    """
    出库明细响应模型：
      - 用于接口返回时展示出库明细行信息
      - 包含数据库主键 id 字段，便于前端做行级操作（例如查看、后续扩展）
    """
    id: int
    product_id: int
    quantity: int
    unit_price: Optional[float] = None
    remark: Optional[str] = None

    # 允许从 ORM 模型对象转换（SQLAlchemy 实例 → Pydantic 模型）
    model_config = {
        "from_attributes": True
    }


# ============================================================
# 出库单（OutboundOrder）相关模型
# ============================================================

class OutboundOrderCreate(BaseModel):
    """
    出库单创建入参模型：
      - 用于前端创建出库单时提交的数据结构
      - 不包含 order_no（出库单号），由后端在 Service 层自动生成
      - 必须传入仓库ID、出库明细列表；客户与出库类型可选
    """
    warehouse_id: int = Field(..., gt=0, description="出库仓库ID，对应 warehouses.id")
    customer: Optional[str] = Field(
        default=None,
        max_length=100,
        description="客户/接收方名称，例如某公司、某门店、某个人"
    )
    outbound_type: Optional[str] = Field(
        default=None,
        max_length=30,
        description="出库类型，例如 sale(销售出库)/transfer(调拨出库)/return(退货出库)"
    )
    items: List[OutboundItemCreate] = Field(
        ...,
        description="出库明细列表，至少包含一条明细"
    )


class OutboundOrderUpdate(BaseModel):
    """
    出库单状态更新模型：
      - 用于更新出库单的状态（例如审批、执行、确认）
      - 状态限定为固定几种字符串值，避免传入非法状态
      - 状态流转建议：created → approved → executed → confirmed
    """
    status: str = Field(
        ...,
        pattern="^(created|approved|executed|confirmed)$",
        description="出库单状态，只允许 created/approved/executed/confirmed 之一"
    )


class OutboundOrderInfo(BaseModel):
    """
    出库单响应模型：
      - 用于接口返回出库单详情或列表时的展示结构
      - 包含主键、单号、仓库、客户、状态、时间等基础信息
      - 内嵌明细列表 items，方便前端一次性拿到整单数据
    """
    id: int
    order_no: str
    warehouse_id: int
    customer: Optional[str]
    outbound_type: Optional[str]
    status: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    # 内嵌出库明细信息列表
    items: List[OutboundItemInfo] = []

    model_config = {
        "from_attributes": True
    }
