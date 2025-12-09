"""
@ coding : utf-8 
@Time    : 2025/12/9 17:40
@Author  : admin1
@Project : fastapi_wms
@File    : stocktaking_dao.py
@Desc    :
@Notes   : 盘点模块 Pydantic 数据模型定义
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ============================================================
# 盘点明细（StocktakingItem）相关模型
# ============================================================

class StocktakingItemCreate(BaseModel):
    """
    盘点明细创建模型：
      - 前端录入时提交每个商品的系统数量与实盘数量
      - 差异由后端计算（counted_qty - system_qty）
    """
    product_id: int = Field(..., gt=0, description="商品ID")
    system_qty: int = Field(..., ge=0, description="系统库存数量")
    counted_qty: int = Field(..., ge=0, description="实际盘点数量")
    remark: Optional[str] = Field(None, max_length=255, description="备注信息")


class StocktakingItemInfo(BaseModel):
    """
    盘点明细返回模型：
      - 用于接口返回时展示每一行盘点数据
    """
    id: int
    product_id: int
    system_qty: int
    counted_qty: int
    diff_qty: int
    remark: Optional[str]

    model_config = {
        "from_attributes": True
    }


# ============================================================
# 盘点单（StocktakingOrder）相关模型
# ============================================================

class StocktakingOrderCreate(BaseModel):
    """
    盘点单创建入参模型：
      - 创建盘点任务时传入仓库、备注、盘点明细
    """
    warehouse_id: int = Field(..., gt=0, description="盘点仓库ID")
    remark: Optional[str] = Field(None, max_length=255, description="盘点说明")
    items: List[StocktakingItemCreate] = Field(..., description="盘点明细列表，至少一条")


class StocktakingOrderConfirm(BaseModel):
    """
    盘点确认模型：
      - 用于确认盘点结果时的请求参数
      - 状态流转：created → confirmed
    """
    remark: Optional[str] = Field(None, description="确认备注（可选）")


class StocktakingOrderInfo(BaseModel):
    """
    盘点单响应模型：
      - 用于接口返回完整盘点单详情
    """
    id: int
    order_no: str
    warehouse_id: int
    status: str
    created_by: int
    confirmed_by: Optional[int]
    remark: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[StocktakingItemInfo] = []

    model_config = {
        "from_attributes": True
    }

