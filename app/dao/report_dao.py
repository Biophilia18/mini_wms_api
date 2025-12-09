"""
@ coding : utf-8 
@Time    : 2025/12/9 18:18
@Author  : admin1
@Project : fastapi_wms
@File    : report_dao.py
@Desc    :
@Notes   : 实时报表数据访问层（DAO），用于统计库存、出入库、调拨、盘点差异等信息
"""
from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.inventory import Inventory
from app.models.outbound import OutboundOrder, OutboundItem
from app.models.report import ReportDailySummary
from app.models.transfer import TransferOrder, TransferItem
from app.models.stocktaking import StocktakingOrder, StocktakingItem


class ReportDAO:
    """
    实时报表 DAO 层：
      - 负责聚合查询，不修改业务表数据
      - 提供库存、出入库、调拨、盘点差异四类统计
    """

    # -------------------------------------------------------
    # 库存汇总统计
    # -------------------------------------------------------
    def inventory_summary(self, db: Session):
        """查询各仓库存总量与商品种类"""
        return (
            db.query(
                Inventory.warehouse_id,                         # 仓库ID
                func.count(Inventory.product_id).label("total_products"),  # 商品种类数
                func.sum(Inventory.quantity).label("total_quantity"),      # 总库存量
            )
            .group_by(Inventory.warehouse_id)
            .all()
        )

    # -------------------------------------------------------
    # 出入库汇总统计
    # -------------------------------------------------------
    def inbound_outbound_summary(self, db: Session, start_date=None, end_date=None):
        """统计各仓出库数量，可选时间范围"""
        query_out = (
            db.query(
                OutboundOrder.warehouse_id.label("warehouse_id"),       # 仓库ID
                func.sum(OutboundItem.quantity).label("total_out_qty"), # 出库总数量
            )
            .join(OutboundItem, OutboundOrder.id == OutboundItem.outbound_id)
        )
        if start_date:
            query_out = query_out.filter(OutboundOrder.created_at >= start_date)
        if end_date:
            query_out = query_out.filter(OutboundOrder.created_at <= end_date)
        return query_out.group_by(OutboundOrder.warehouse_id).all()

    # -------------------------------------------------------
    # 调拨汇总统计
    # -------------------------------------------------------
    def transfer_summary(self, db: Session, start_date=None, end_date=None):
        """统计调拨单数量与总调拨量"""
        query = (
            db.query(
                TransferOrder.source_warehouse_id.label("source_warehouse_id"), # 调出仓
                TransferOrder.target_warehouse_id.label("target_warehouse_id"), # 调入仓
                func.count(TransferOrder.id).label("transfer_count"),           # 调拨单数
                func.sum(TransferItem.quantity).label("total_quantity"),        # 调拨总量
            )
            .join(TransferItem, TransferOrder.id == TransferItem.transfer_id)
        )
        # ---- 修正时间过滤 ----
        if start_date:
            if isinstance(start_date, datetime):
                start_dt = start_date
            else:
                start_dt = datetime.combine(start_date, datetime.min.time())
            query = query.filter(TransferOrder.created_at >= start_dt)

        if end_date:
            if isinstance(end_date, datetime):
                end_dt = end_date
            else:
                end_dt = datetime.combine(end_date, datetime.max.time())
            query = query.filter(TransferOrder.created_at <= end_dt)
        return query.group_by(
            TransferOrder.source_warehouse_id, TransferOrder.target_warehouse_id
        ).all()

    # -------------------------------------------------------
    # 盘点差异统计
    # -------------------------------------------------------
    def stocktaking_diff_summary(self, db: Session):
        """统计盘点差异数量（counted_qty - system_qty）"""
        return (
            db.query(
                StocktakingOrder.warehouse_id,                              # 仓库ID
                func.count(StocktakingOrder.id).label("order_count"),       # 盘点单数
                func.sum(StocktakingItem.diff_qty).label("total_diff_qty"), # 差异合计
            )
            .join(StocktakingItem, StocktakingOrder.id == StocktakingItem.stocktaking_id)
            .group_by(StocktakingOrder.warehouse_id)
            .all()
        )

# 日报表
class ReportDailyDAO:
    """
    负责日报表的查询与写入
    """

    def get_by_date(self, db: Session, target_date: date):
        """按日期查询"""
        return db.query(ReportDailySummary).filter(
            ReportDailySummary.date == target_date
        ).first()

    def get_list(self, db: Session, start_date: date, end_date: date):
        """按时间区间查询"""
        return (
            db.query(ReportDailySummary)
            .filter(
                ReportDailySummary.date >= start_date,
                ReportDailySummary.date <= end_date,
            )
            .order_by(ReportDailySummary.date.desc())
            .all()
        )

    def insert(self, db: Session, summary: ReportDailySummary):
        """插入日报记录"""
        db.add(summary)
        db.commit()
        db.refresh(summary)
        return summary

    def delete_existing(self, db: Session, target_date: date):
        """删除旧归档"""
        db.query(ReportDailySummary).filter(
            ReportDailySummary.date == target_date
        ).delete()
        db.commit()