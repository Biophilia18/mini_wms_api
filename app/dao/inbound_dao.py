"""
@ coding : utf-8 
@Time    : 2025/12/8 21:00
@Author  : admin1
@Project : fastapi_wms
@File    : inbound_dao.py
@Desc    :
@Notes   : 入库模块dao层定义
"""
from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.inbound_order import InboundOrder, InboundItem


class InboundOrderDAO(BaseDAO[InboundOrder]):
    """入库单DAO层"""
    def __init__(self):
        super().__init__(InboundOrder)

    def get_by_order_no(self, db: Session, order_no:str):
        """根据入库单号查询"""
        return db.query(InboundOrder).filter(InboundOrder.order_no == order_no).first()

    def list_by_warehouse(self, db: Session, warehouse_id: int):
        """查询指定仓库的入库单"""
        return (
            db.query(InboundOrder)
            .filter(InboundOrder.warehouse_id == warehouse_id)
            .order_by(InboundOrder.created_at.desc())
            .all()
        )

    def list_by_user(self, db: Session, user_id: int):
        """查询某用户创建的入库单"""
        return (
            db.query(InboundOrder)
            .filter(InboundOrder.created_by == user_id)
            .order_by(InboundOrder.created_at.desc())
            .all()
        )

class InboundItemDAO(BaseDAO[InboundItem]):
    """入库单明细DAO层"""
    def __init__(self):
        super().__init__(InboundItem)

    def list_by_inbound_id(self, db: Session, inbound_id: int):
        """查询某入库单下的所有明细"""
        return (
            db.query(InboundItem)
            .filter(InboundItem.inbound_id == inbound_id)
            .all()
        )

    def delete_by_inbound_id(self, db: Session, inbound_id: int):
        """删除指定入库单的所有明细：用于重建"""
        db.query(InboundItem).filter(InboundItem.inbound_id == inbound_id).delete()
        db.commit()