"""
@ coding : utf-8 
@Time    : 2025/12/8 22:47
@Author  : admin1
@Project : fastapi_wms
@File    : outbound_service.py
@Desc    :
@Notes   : 出库单数据访问层（DAO）定义
"""

from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.outbound import OutboundOrder, OutboundItem


class OutboundOrderDAO(BaseDAO[OutboundOrder]):
    """
    出库单主表 DAO：
      - 继承 BaseDAO，实现基础的 CRUD 操作（create, get, update, delete）
      - 封装针对出库业务的专用查询，如按单号查询、按用户查询等
    """
    def __init__(self):
        super().__init__(OutboundOrder)

    def get_by_order_no(self, db: Session, order_no: str):
        """
        根据出库单号查询单据。
        常用于执行、确认等操作时，通过单号快速定位单据对象。
        """
        return db.query(self.model).filter(self.model.order_no == order_no).first()

    def get_by_user(self, db: Session, user_id: int):
        """
        查询指定用户创建的所有出库单。
        一般用于“出库单列表”接口，根据登录用户ID筛选。
        """
        return (
            db.query(self.model)
            .filter(self.model.created_by == user_id)
            .order_by(self.model.created_at.desc())
            .all()
        )


class OutboundItemDAO(BaseDAO[OutboundItem]):
    """
    出库单明细表 DAO：
      - 用于操作 outbound_items 表
      - 支持按出库单ID或商品ID查询明细
    """
    def __init__(self):
        super().__init__(OutboundItem)

    def get_by_outbound_id(self, db: Session, outbound_id: int):
        """
        查询指定出库单下的所有明细行。
        通常在接口层用于加载单据详情。
        """
        return (
            db.query(self.model)
            .filter(self.model.outbound_id == outbound_id)
            .all()
        )

    def get_product_in_outbound(self, db: Session, outbound_id: int, product_id: int):
        """
        查询某出库单中某商品的出库行（若存在）。
        常用于检查重复添加或行级校验。
        """
        return (
            db.query(self.model)
            .filter(
                self.model.outbound_id == outbound_id,
                self.model.product_id == product_id,
            )
            .first()
        )
