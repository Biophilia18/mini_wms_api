"""
@ coding : utf-8 
@Time    : 2025/12/9 18:20
@Author  : admin1
@Project : fastapi_wms
@File    : report.py
@Desc    :
@Notes   : 报表统计模块接口控制层（Controller）
"""
from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.base import ResponseModel
from app.schemas.report import (
    ReportDateRange,
    InventorySummary,
    InboundOutboundSummary,
    TransferSummary,
    StocktakingDiffSummary, DailySummaryInfo, DailyArchiveRequest, DailySummaryList,
)
from app.services.report_service import ReportService


# ============================================================
# 路由初始化
# ============================================================

rt_report = APIRouter(prefix="/report", tags=["统计报表"])
service = ReportService()


# ============================================================
# 实时库存统计
# ============================================================

@rt_report.get("/inventory", response_model=ResponseModel[List[InventorySummary]])
def get_inventory_report(db: Session = Depends(get_db)):
    """
    实时库存统计接口：
      - 汇总每个仓库的库存总量与商品种类数
    """
    try:
        data = service.get_inventory_summary(db)
        return ResponseModel(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 出入库统计
# ============================================================

@rt_report.post("/inout", response_model=ResponseModel[List[InboundOutboundSummary]])
def get_inout_report(req: ReportDateRange, db: Session = Depends(get_db)):
    """
    出入库统计接口：
      - 支持按日期区间查询
      - 当前实现仅统计出库数量（入库预留扩展）
    """
    try:
        data = service.get_inbound_outbound_summary(db, req.start_date, req.end_date)
        return ResponseModel(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 调拨统计
# ============================================================

@rt_report.post("/transfer", response_model=ResponseModel[List[TransferSummary]])
def get_transfer_report(
    body: ReportDateRange,
    db: Session = Depends(get_db),
):
    """
    调拨汇总报表：
      - 支持传入日期范围
      - 默认统计本月所有调拨
    """
    try:
        start_date = body.start_date or date.today().replace(day=1)
        end_date = body.end_date or date.today()
        data = service.get_transfer_summary(db, start_date, end_date)
        return ResponseModel(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 盘点差异统计
# ============================================================

@rt_report.get("/stocktaking", response_model=ResponseModel[List[StocktakingDiffSummary]])
def get_stocktaking_report(db: Session = Depends(get_db)):
    """
    盘点差异统计接口：
      - 汇总各仓盘点单数量与差异总数
    """
    try:
        data = service.get_stocktaking_diff_summary(db)
        return ResponseModel(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@rt_report.post("/archive/daily", response_model=ResponseModel[DailySummaryInfo])
def create_daily_report(req: DailyArchiveRequest, db: Session = Depends(get_db)):
    """
    手动触发日报表归档：
      - 默认统计前一天
      - 聚合出入库、调拨、盘点差异
    """
    try:
        target_date = req.target_date or (date.today() - timedelta(days=1))
        summary = service.create_daily_summary(db, target_date, req.remark)
        return ResponseModel(data=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@rt_report.get("/archive/list", response_model=ResponseModel[DailySummaryList])
def list_daily_reports(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    """按日期区间查询日报表"""
    data = service.list_daily_summaries(db, start_date, end_date)
    return ResponseModel(data={"summaries": data})

@rt_report.get("/archive/{target_date}", response_model=ResponseModel[DailySummaryInfo])
def get_daily_report(target_date: date, db: Session = Depends(get_db)):
    """查询指定日期的日报表"""
    summary = service.get_daily_summary(db, target_date)
    if not summary:
        raise HTTPException(status_code=404, detail="未找到对应日期的日报表")
    return ResponseModel(data=summary)
    # 动态路径参数必须放在固定路径之后，否则会错误解析路径字符串
