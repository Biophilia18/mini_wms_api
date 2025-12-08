"""
@ coding : utf-8 
@Time    : 2025/12/8 17:56
@Author  : admin1
@Project : fastapi_wms
@File    : inbound_order.py
@Desc    :
@Notes   : 入库单表
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base




class InboundOrder(Base):
    """
    入库单主表：
      - 用于记录一次入库业务（例如：某供应商向某仓库发货）
      - 一个入库单可以包含多条入库明细
    """
    __tablename__ = "inbound_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, index=True, nullable=False, comment="入库单号")
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="入库仓库ID")
    supplier = Column(String(100), nullable=True, comment="供应商名称")
    # created, approved, executed, confirmed
    status = Column(String(20), default="created", nullable=False, comment="单据状态")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建人ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="最后更新时间")

    # 关系映射
    warehouse = relationship("Warehouse", backref="inbound_orders")
    creator = relationship("User", backref="created_inbound_orders")
    items = relationship(
        "InboundItem",
        back_populates="inbound_order",
        cascade="all, delete-orphan" # 删除入库单时自动删除对应明细，避免“孤儿行数据”；
    )


class InboundItem(Base):
    """
    入库单明细表：
      - 记录具体入库的商品、数量、单价等
      - 与入库单为 1:N 关系
    """
    __tablename__ = "inbound_items"

    id = Column(Integer, primary_key=True, index=True)
    inbound_id = Column(Integer, ForeignKey("inbound_orders.id"), nullable=False, comment="入库单ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")
    quantity = Column(Integer, nullable=False, comment="入库数量")
    unit_price = Column(Float, nullable=True, comment="入库单价（含税）")
    remark = Column(String(255), nullable=True, comment="行备注")

    # 关系映射
    inbound_order = relationship("InboundOrder", back_populates="items")
    product = relationship("Product", backref="inbound_items")