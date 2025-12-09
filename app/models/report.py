"""
@ coding : utf-8 
@Time    : 2025/12/9 19:15
@Author  : admin1
@Project : fastapi_wms
@File    : report.py
@Desc    :
@Notes   : 日报表数据模型（用于每日定时归档统计）
"""

from sqlalchemy import Column, Integer, Date, String, Float, func
from app.database import Base

class ReportDailySummary(Base):
    """
    日报表模型：
      - 每天一条记录（可按仓库维度）
      - 存储每日出入库、调拨、盘点差异等关键指标
    """
    __tablename__ = "report_daily_summary"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, comment="统计日期")
    warehouse_id = Column(Integer, nullable=True, comment="仓库ID（可空，全局汇总）")

    inbound_qty = Column(Integer, default=0, comment="入库总数量")
    outbound_qty = Column(Integer, default=0, comment="出库总数量")
    transfer_qty = Column(Integer, default=0, comment="调拨总数量")
    stock_diff_qty = Column(Integer, default=0, comment="盘点差异数量")

    remark = Column(String(255), nullable=True, comment="备注信息")
    created_at = Column(Date, server_default=func.now(), comment="记录创建日期")
