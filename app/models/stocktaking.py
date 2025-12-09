"""
@ coding : utf-8 
@Time    : 2025/12/9 17:31
@Author  : admin1
@Project : fastapi_wms
@File    : stocktaking_dao.py
@Desc    :
@Notes   : 盘点单与盘点明细模型定义
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class StocktakingOrder(Base):
    """
    盘点单主表：
      - 记录某个仓库的一次库存盘点任务
      - 包含多条盘点明细（StocktakingItem）
      - 状态简单设计为：created / confirmed
    """
    __tablename__ = "stocktaking_orders"

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")  # 主键ID
    order_no = Column(String(50), unique=True, index=True, nullable=False, comment="盘点单号")  # 盘点单号
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="盘点仓库ID")  # 仓库ID
    status = Column(String(20), default="created", nullable=False, comment="单据状态")  # created / confirmed
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建人ID")  # 创建人
    confirmed_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="确认人ID")  # 确认人
    remark = Column(String(255), nullable=True, comment="盘点说明备注")  # 备注

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="最后更新时间")  # 更新时间

    # 关联：仓库
    warehouse = relationship("Warehouse", backref="stocktaking_orders")
    # 关联：创建人
    creator = relationship("User", foreign_keys='StocktakingOrder.created_by', backref="created_stocktaking_orders")
    # 关联：确认人
    confirmer = relationship("User", foreign_keys="StocktakingOrder.confirmed_by", backref="confirmed_stocktaking_orders")
    # 关联：盘点明细列表
    items = relationship(
        "StocktakingItem",
        back_populates="stocktaking_order",
        cascade="all, delete-orphan"
    )


class StocktakingItem(Base):
    """
    盘点明细表：
      - 记录某次盘点中某个商品的系统数量、实盘数量及差异
    """
    __tablename__ = "stocktaking_items"

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")  # 主键ID
    stocktaking_id = Column(Integer, ForeignKey("stocktaking_orders.id"), nullable=False, comment="盘点单ID")  # 所属盘点单
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")  # 商品ID

    system_qty = Column(Integer, nullable=False, comment="系统库存数量")  # 盘点时系统数量
    counted_qty = Column(Integer, nullable=False, comment="实盘数量")  # 实际盘点数量
    diff_qty = Column(Integer, nullable=False, comment="差异数量")  # counted_qty - system_qty

    remark = Column(String(255), nullable=True, comment="盘点明细备注")  # 备注

    # 关联：盘点单
    stocktaking_order = relationship("StocktakingOrder", back_populates="items")
    # 关联：商品
    product = relationship("Product", backref="stocktaking_items")
