"""
@ coding : utf-8 
@Time    : 2025/10/26 10:57
@Author  : admin
@Project : fastapi_wms
@File    : stock_log.py
@Software: PyCharm
@Notes   : 出入库日志表模型
"""
import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class StockAction(str, enum.Enum):
    IN = 'in' # 入库
    OUT = 'out' # 出库
    ADJUST = 'adjust'  #盘点调整

class StockLog(Base):
    __tablename__ = 'stock_logs'
    id = Column(Integer, primary_key=True,index=True)
    inventory_id = Column(Integer, ForeignKey('inventories.id'),nullable=False, comment="库存记录id")
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False, comment="操作人")
    action = Column(Enum(StockAction), nullable=False, comment="操作类型")
    change_qty = Column(Integer, nullable=False, comment="变动数量")
    remark = Column(Text, nullable=True, comment="备注")
    created_at = Column(DateTime, server_default=func.now(),comment="操作时间")

    # 关系定义
    inventory = relationship("Inventory", backref="stock_logs")
    user = relationship("User", backref="stock_logs")


