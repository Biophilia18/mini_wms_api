"""
@ coding : utf-8 
@Time    : 2025/12/9 17:41
@Author  : admin1
@Project : fastapi_wms
@File    : stocktaking_dao.py
@Desc    :
@Notes   : 盘点模块数据访问层（DAO）
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.dao.base import BaseDAO
from app.models.stocktaking import StocktakingOrder, StocktakingItem


class StocktakingOrderDAO(BaseDAO[StocktakingOrder]):
    """盘点单主表 DAO"""

    def __init__(self):
        super().__init__(StocktakingOrder)

    def get_by_order_no(self, db: Session, order_no: str) -> Optional[StocktakingOrder]:
        """根据盘点单号查询单据"""
        return db.query(self.model).filter(self.model.order_no == order_no).first()

    def list_orders(self, db: Session, created_by: Optional[int] = None, skip: int = 0, limit: int = 50) -> List[StocktakingOrder]:
        """按创建人查询盘点单列表"""
        query = db.query(self.model).order_by(desc(self.model.created_at))
        if created_by:
            query = query.filter(self.model.created_by == created_by)
        return query.offset(skip).limit(limit).all()


class StocktakingItemDAO(BaseDAO[StocktakingItem]):
    """盘点单明细表 DAO"""

    def __init__(self):
        super().__init__(StocktakingItem)

    def list_by_order(self, db: Session, stocktaking_id: int) -> List[StocktakingItem]:
        """按盘点单ID查询所有明细"""
        return db.query(self.model).filter(self.model.stocktaking_id == stocktaking_id).all()

    def get_by_product(self, db: Session, stocktaking_id: int, product_id: int) -> Optional[StocktakingItem]:
        """查询某盘点单下某商品明细"""
        return (
            db.query(self.model)
            .filter(
                self.model.stocktaking_id == stocktaking_id,
                self.model.product_id == product_id,
            )
            .first()
        )
