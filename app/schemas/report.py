"""
@ coding : utf-8 
@Time    : 2025/12/9 18:16
@Author  : admin1
@Project : fastapi_wms
@File    : report_dao.py
@Desc    :
@Notes   : 报表统计模块 Pydantic 数据模型定义
"""

from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field


# ============================================================
# 公共时间区间模型
# ============================================================

class ReportDateRange(BaseModel):
    """
    报表统计时间区间模型：
      - 用于按日期范围查询出入库、调拨统计
      - 可选 start_date 与 end_date
    """
    start_date: Optional[date] = Field(None, description="起始日期（可选）")
    end_date: Optional[date] = Field(None, description="结束日期（可选）")


# ============================================================
# 库存统计模型
# ============================================================

class InventorySummary(BaseModel):
    """
    仓库库存汇总模型：
      - 展示每个仓的库存商品数与总库存量
    """
    warehouse_id: int = Field(..., description="仓库ID")
    total_products: int = Field(..., description="商品种类数")
    total_quantity: int = Field(..., description="库存总数量")

    model_config = {
        "from_attributes": True
    }


# ============================================================
# 出入库统计模型
# ============================================================

class InboundOutboundSummary(BaseModel):
    """
    出入库汇总模型：
      - 展示每个仓的出库数量统计
      - 入库暂留扩展接口
    """
    warehouse_id: int = Field(..., description="仓库ID")
    total_out_qty: int = Field(..., description="出库总数量")

    model_config = {
        "from_attributes": True
    }


# ============================================================
# 调拨统计模型
# ============================================================

class TransferSummary(BaseModel):
    """
    调拨汇总模型：
      - 展示各仓之间的调拨单数量与总调拨量
    """
    source_warehouse_id: int = Field(..., description="调出仓ID")
    target_warehouse_id: int = Field(..., description="调入仓ID")
    transfer_count: int = Field(..., description="调拨单数量")
    total_quantity: int = Field(..., description="调拨总数量")

    model_config = {
        "from_attributes": True
    }


# ============================================================
# 盘点差异统计模型
# ============================================================

class StocktakingDiffSummary(BaseModel):
    """
    盘点差异统计模型：
      - 展示各仓盘点单数量与差异数量合计
    """
    warehouse_id: int = Field(..., description="仓库ID")
    order_count: int = Field(..., description="盘点单数量")
    total_diff_qty: int = Field(..., description="差异数量合计")

    model_config = {
        "from_attributes": True
    }

# 日报表归档模型
class DailyArchiveRequest(BaseModel):
    """
    日报表归档请求模型：
      - 允许手动触发指定日期的汇总（通常是昨天）
      - 不传则默认归档前一日
    """
    target_date: Optional[date] = Field(None, description="指定归档日期（默认昨天）")
    remark: Optional[str] = Field(None, max_length=255, description="备注信息（可选）")


class DailySummaryInfo(BaseModel):
    """
    日报表信息模型：
      - 用于接口返回归档结果或历史记录
      - 对应数据库表 report_daily_summary
    """
    id: int
    date: date
    warehouse_id: Optional[int]
    inbound_qty: int
    outbound_qty: int
    transfer_qty: int
    stock_diff_qty: int
    remark: Optional[str]

    model_config = {
        "from_attributes": True
    }


class DailySummaryList(BaseModel):
    """
    日报表列表响应模型：
      - 用于返回多日汇总记录
    """
    summaries: List[DailySummaryInfo]

    model_config = {
        "from_attributes": True
    }
