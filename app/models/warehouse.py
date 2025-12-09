"""
@ coding : utf-8 
@Time    : 2025/10/25 17:13
@Author  : admin
@Project : fastapi_wms
@File    : warehouse.py
@Software: PyCharm
@Notes   : 仓库表模型，管理物理存储位置
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, comment="仓库名称")
    code = Column(String(20), unique=True, nullable=False, comment="仓库编码")
    address = Column(String(200), comment="仓库地址")
    capacity = Column(Integer, comment="仓库容量（总货位数）")
    manager_id = Column(Integer, ForeignKey("users.id"), comment="仓库管理员ID")
    is_active = Column(Boolean, default=True, comment="是否启用")

    # 关系定义
    #  Warehouse ↔ User(N: 1) - 多个仓库可由一个用户管理
    #  Warehouse ↔ Inventory(1: N) - 一个仓库包含多个商品库存
    manager = relationship("User", backref="managed_warehouses")
    # 一个仓库有多个库存记录
    inventories = relationship("Inventory", back_populates="warehouse")
