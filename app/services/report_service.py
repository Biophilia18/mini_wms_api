"""
@ coding : utf-8 
@Time    : 2025/12/09 18:50
@Author  : admin1
@Project : fastapi_wms
@File    : report_service.py
@Desc    :
@Notes   : 实时报表业务逻辑层（Service），将 DAO 聚合结果转换为 Pydantic 模型，避免 Row 序列化问题
"""
from datetime import date
from typing import Iterable, Type, TypeVar, List

from sqlalchemy.orm import Session

from app.dao.report_dao import ReportDAO, ReportDailyDAO
from app.models.report import ReportDailySummary
from app.schemas.report import (
    InventorySummary,
    InboundOutboundSummary,
    TransferSummary,
    StocktakingDiffSummary,
)

# 泛型：用于通用 Row → Pydantic 模型转换
TModel = TypeVar("TModel")


class ReportService:
    """
    实时报表 Service 层：
      - 调用 ReportDAO 执行聚合查询
      - 将 SQLAlchemy Row 转换为 Pydantic 模型列表
    """

    def __init__(self):
        self.dao = ReportDAO()
        self.daily_dao = ReportDailyDAO()

    # 通用工具方法：Row 列表 → Pydantic 模型列表
    @staticmethod
    def _rows_to_models(rows: Iterable, model_cls: Type[TModel]) -> List[TModel]:
        """
        将 SQLAlchemy Row 结果转换为 Pydantic 模型列表：
          - Row._mapping 是一个 Mapping，可转为 dict 作为模型入参
          - 解决 FastAPI 无法序列化 Row 类型的问题
        """
        return [model_cls(**dict(row._mapping)) for row in rows]

    # -------------------------------------------------------
    # 库存统计
    # -------------------------------------------------------
    def get_inventory_summary(self, db: Session) -> List[InventorySummary]:
        """获取仓库库存汇总信息（转换为 InventorySummary 列表）"""
        rows = self.dao.inventory_summary(db)
        return self._rows_to_models(rows, InventorySummary)

    # -------------------------------------------------------
    # 出入库统计
    # -------------------------------------------------------
    def get_inbound_outbound_summary(
        self,
        db: Session,
        start_date=None,
        end_date=None,
    ) -> List[InboundOutboundSummary]:
        """获取出入库汇总统计（当前实现仅统计出库数量）"""
        rows = self.dao.inbound_outbound_summary(db, start_date, end_date)
        return self._rows_to_models(rows, InboundOutboundSummary)

    # -------------------------------------------------------
    # 调拨统计
    # -------------------------------------------------------
    def get_transfer_summary(
        self,
        db: Session,
        start_date=None,
        end_date=None,
    ) -> List[TransferSummary]:
        """获取调拨单统计信息"""
        rows = self.dao.transfer_summary(db, start_date, end_date)
        return self._rows_to_models(rows, TransferSummary)

    # -------------------------------------------------------
    # 盘点差异统计
    # -------------------------------------------------------
    def get_stocktaking_diff_summary(self, db: Session) -> List[StocktakingDiffSummary]:
        """获取盘点差异统计结果"""
        rows = self.dao.stocktaking_diff_summary(db)
        return self._rows_to_models(rows, StocktakingDiffSummary)

# -------------------------------------------------------
    # 创建每日汇总
    # -------------------------------------------------------
    def create_daily_summary(self, db: Session, target_date: date, remark: str = None):
        """
        根据实时汇总生成日报表记录：
          1. 删除旧记录
          2. 聚合四类指标（出库、入库、调拨、盘点）
          3. 写入 report_daily_summary
        """
        # 删除旧记录
        self.daily_dao.delete_existing(db, target_date)

        # 聚合实时统计数据
        out_summary = self.dao.inbound_outbound_summary(db)
        transfer_summary = self.dao.transfer_summary(db)
        stock_diff = self.dao.stocktaking_diff_summary(db)

        total_out = sum(row.total_out_qty or 0 for row in out_summary)
        total_transfer = sum(row.total_quantity or 0 for row in transfer_summary)
        total_diff = sum(row.total_diff_qty or 0 for row in stock_diff)

        summary = ReportDailySummary(
            date=target_date,
            inbound_qty=0,  # 入库后续可补
            outbound_qty=total_out,
            transfer_qty=total_transfer,
            stock_diff_qty=total_diff,
            remark=remark,
        )
        return self.daily_dao.insert(db, summary)

    # -------------------------------------------------------
    # 查询
    # -------------------------------------------------------
    def get_daily_summary(self, db: Session, target_date: date):
        return self.daily_dao.get_by_date(db, target_date)

    def list_daily_summaries(self, db: Session, start_date: date, end_date: date):
        return self.daily_dao.get_list(db, start_date, end_date)