"""
@ coding : utf-8
@Time    : 2025/12/9 10:02
@Author  : admin1
@Project : fastapi_wms
@File    : transfer.py
@Desc    : 仓库调拨单与调拨明细表模型定义
"""
from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from app.database import Base


class TransferOrder(Base):
    """调拨单主表：记录仓库间库存调拨"""
    __tablename__ = "transfer_orders"

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")  # 主键ID
    transfer_no = Column(String(50), unique=True, index=True, nullable=False, comment="调拨单号")  # 单号
    source_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="调出仓库ID")  # 调出仓库
    target_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="调入仓库ID")  # 调入仓库
    status = Column(String(20), default="created", nullable=False,comment="单据状态")  # 状态：created/approved/executed/confirmed
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建人ID")  # 创建人
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="审核人ID")  # 审批人
    executed_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="执行人ID")  # 执行人
    remark = Column(String(255), nullable=True, comment="备注")  # 备注信息
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")  # 更新时间

    source_warehouse = relationship("Warehouse", foreign_keys="TransferOrder.source_warehouse_id",
                                    backref="transfer_out_orders")  # 调出仓库对象
    target_warehouse = relationship("Warehouse", foreign_keys="TransferOrder.target_warehouse_id",
                                    backref="transfer_in_orders")  # 调入仓库对象
    creator = relationship("User", foreign_keys="TransferOrder.created_by",
                           backref="created_transfer_orders")  # 创建人对象
    approver = relationship("User", foreign_keys="TransferOrder.approved_by",
                            backref="approved_transfer_orders")  # 审批人对象
    executor = relationship("User", foreign_keys="TransferOrder.executed_by",
                            backref="executed_transfer_orders")  # 执行人对象
    items = relationship("TransferItem", back_populates="transfer_order", cascade="all, delete-orphan")  # 明细列表


class TransferItem(Base):
    """调拨单明细表：记录商品及数量"""
    __tablename__ = "transfer_items"

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")  # 主键ID
    transfer_id = Column(Integer, ForeignKey("transfer_orders.id"), nullable=False, comment="调拨单ID")  # 所属调拨单
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")  # 商品ID
    quantity = Column(Integer, nullable=False, comment="调拨数量")  # 调拨数量
    unit_price = Column(Float, nullable=True, comment="单价")  # 单价（可选，用于成本核算）
    remark = Column(String(255), nullable=True, comment="备注")  # 明细备注

    transfer_order = relationship("TransferOrder", back_populates="items")  # 主单对象
    product = relationship("Product", backref="transfer_items")  # 商品对象


class TransferStatus(str, Enum):
    """
    调拨单状态枚举：
      - 保证状态流转合法、可读性强
      - 用于数据库字段 status 的业务枚举控制
    """
    CREATED = "created"  # 新建：草稿状态，等待审批
    APPROVED = "approved"  # 已审批：允许执行
    EXECUTED = "executed"  # 已执行：库存已调整
    CONFIRMED = "confirmed"  # 已确认：业务完成

    @classmethod
    def choices(cls) -> list[str]:
        """返回所有可选状态列表"""
        return [status.value for status in cls]
