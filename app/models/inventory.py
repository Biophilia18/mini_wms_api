"""
@ coding : utf-8 
@Time    : 2025/10/26 09:16
@Author  : admin
@Project : fastapi_wms
@File    : inventory.py
@Software: PyCharm
@Notes   : 库存表模型，管理商品在仓库中的数量
"""
from sqlalchemy import Column, Integer,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Inventory(Base):
    __tablename__ = 'inventories'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'),nullable=False, comment="商品id")
    warehouse_id = Column(Integer,ForeignKey('warehouses.id'),nullable=False, comment="仓库id")
    quantity = Column(Integer, nullable=False, default=0, comment="当前库存数量")
    # 关系定义
    product = relationship("Product", backref="inventories")
    warehouse = relationship("Warehouse", backref="inventories")

    # 一个仓库中一个商品只能有一条库存记录
    __table_args__ = (
        UniqueConstraint('product_id', 'warehouse_id', name='uq_product_warehouse'),
    )
