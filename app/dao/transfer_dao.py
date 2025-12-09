"""
@ coding : utf-8
@Time    : 2025/12/10 00:05
@Author  : admin1
@Project : fastapi_wms
@File    : transfer.py
@Desc    :
@Notes   : 调拨单数据访问层（DAO）定义
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.dao.base import BaseDAO
from app.models.transfer import TransferOrder, TransferItem


class TransferOrderDAO(BaseDAO[TransferOrder]):
    """
    调拨单主表 DAO：
      - 继承 BaseDAO，提供基础 CRUD 操作
      - 封装调拨单特有的查询逻辑，如按单号、用户或仓库筛选
    """

    def __init__(self):
        super().__init__(TransferOrder)

    def get_by_transfer_no(self, db: Session, transfer_no: str):
        """
        根据调拨单号查询调拨单。
        常用于执行、审批、确认等接口快速定位单据。
        """
        return db.query(self.model).filter(self.model.transfer_no == transfer_no).first()

    def get_by_user(self, db: Session, user_id: int):
        """
        查询指定用户创建的所有调拨单。
        一般用于“调拨单列表”接口。
        """
        return (
            db.query(self.model)
            .filter(self.model.created_by == user_id)
            .order_by(desc(self.model.created_at))
            .all()
        )

    def get_by_warehouse(self, db: Session, warehouse_id: int):
        """
        查询指定仓库（调出或调入）相关的调拨单。
        可用于仓库级别的调拨记录查询。
        """
        return (
            db.query(self.model)
            .filter(
                (self.model.source_warehouse_id == warehouse_id)
                | (self.model.target_warehouse_id == warehouse_id)
            )
            .order_by(desc(self.model.created_at))
            .all()
        )


class TransferItemDAO(BaseDAO[TransferItem]):
    """
    调拨单明细表 DAO：
      - 操作 transfer_items 表
      - 提供按调拨单ID或商品ID查询方法
    """

    def __init__(self):
        super().__init__(TransferItem)

    def get_by_transfer_id(self, db: Session, transfer_id: int):
        """
        查询指定调拨单下的所有明细行。
        常用于详情页加载或执行调拨时校验。
        """
        return (
            db.query(self.model)
            .filter(self.model.transfer_id == transfer_id)
            .all()
        )

    def get_product_in_transfer(self, db: Session, transfer_id: int, product_id: int):
        """
        查询某调拨单中是否存在指定商品的调拨行。
        可用于防止重复添加或行级校验。
        """
        return (
            db.query(self.model)
            .filter(
                self.model.transfer_id == transfer_id,
                self.model.product_id == product_id,
            )
            .first()
        )
