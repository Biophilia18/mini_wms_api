"""
@ coding : utf-8 
@Time    : 2025/12/8 22:36
@Author  : admin1
@Project : fastapi_wms
@File    : outbound_service.py
@Desc    :
@Notes   : 出库单与出库明细模型定义
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship

from app.database import Base


class OutboundOrder(Base):
    """
    出库单主表模型：
      - 用于记录一次“从仓库把货物发出去”的业务行为（例如销售发货、调拨出库等）
      - 一个出库单可以包含多条出库明细记录（OutboundItem）
      - 与仓库（Warehouse）、用户（User）、出库明细（OutboundItem）建立 ORM 关联关系
    """
    __tablename__ = "outbound_orders"

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    # 出库单号：例如 OUT20251208224501，用于业务唯一标识和对账
    order_no = Column(String(50), unique=True, index=True, nullable=False, comment="出库单号")
    # 出库所属仓库ID，对应 warehouses.id
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="出库仓库ID")
    # 可以关联到“客户名称”或“下游接收方”，便于业务对账和查询
    customer = Column(String(100), nullable=True, comment="客户/接收方名称")
    # 出库类型（可选扩展）：如销售出库、调拨出库、退货出库等，当前简单用字符串描述
    outbound_type = Column(String(30), nullable=True, comment="出库类型，例如 sale/transfer/return")
    # 单据状态：created(新建) → approved(已审核) → executed(已执行出库) → confirmed(已确认完成)
    status = Column(String(20), default="created", nullable=False, comment="单据状态")
    # 创建人ID，对应 users.id，记录是谁发起的出库单
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建人ID")
    # 创建时间：由数据库自动填充当前时间
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    # 最后更新时间：在记录被更新时自动写入当前时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="最后更新时间")

    # 关联关系：出库单所属仓库对象
    warehouse = relationship("Warehouse", backref="outbound_orders")
    # 关联关系：出库单创建人（用户）对象
    creator = relationship("User", backref="created_outbound_orders")
    # 关联关系：出库明细列表
    # cascade='all, delete-orphan' 表示删除出库单时，自动删除对应的所有明细行，避免孤儿数据
    items = relationship(
        "OutboundItem",
        back_populates="outbound_order",
        cascade="all, delete-orphan"
    )


class OutboundItem(Base):
    """
    出库单明细表模型：
      - 记录出库单中每一行具体出库的商品、数量、单价等信息
      - 与出库单（OutboundOrder）为 1:N 关系
      - 与商品（Product）建立关联，便于联查商品信息
    """
    __tablename__ = "outbound_items"

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    # 所属出库单ID，对应 outbound_orders.id
    outbound_id = Column(Integer, ForeignKey("outbound_orders.id"), nullable=False, comment="出库单ID")
    # 商品ID，对应 products.id
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")
    # 出库数量，必须为正整数
    quantity = Column(Integer, nullable=False, comment="出库数量")
    # 出库单价（含税），可以为空（例如历史订单不关心价格，仅关心数量）
    unit_price = Column(Float, nullable=True, comment="出库单价（含税）")
    # 行备注：例如特殊说明、批次号、拣货要求等
    remark = Column(String(255), nullable=True, comment="行备注")

    # 关联关系：出库单主表对象
    outbound_order = relationship("OutboundOrder", back_populates="items")
    # 关联关系：商品对象
    product = relationship("Product", backref="outbound_items")
