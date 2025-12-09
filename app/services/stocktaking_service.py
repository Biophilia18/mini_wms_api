"""
@ coding : utf-8 
@Time    : 2025/12/9 17:43
@Author  : admin1
@Project : fastapi_wms
@File    : stocktaking_service.py
@Desc    :
@Notes   : 盘点业务逻辑层（Service）
"""

from datetime import datetime
from sqlalchemy.orm import Session

from app.dao.inventory_dao import InventoryDAO
from app.dao.stock_log_dao import StockLogDAO
from app.dao.stocktaking_dao import StocktakingOrderDAO, StocktakingItemDAO
from app.models.product import Product
from app.models.stock_log import StockAction
from app.models.stocktaking import StocktakingOrder, StocktakingItem
from app.schemas.stocktaking import StocktakingOrderCreate


def generate_stocktaking_no() -> str:
    """生成盘点单号"""
    now = datetime.now()
    return f"STK{now.strftime('%Y%m%d%H%M%S')}"


class StocktakingService:
    """
    盘点模块业务逻辑：
      - 创建盘点单（记录系统数量）
      - 确认盘点（调整差异 + 写入库存日志）
      - 查询盘点单列表
    """

    def __init__(self):
        self.order_dao = StocktakingOrderDAO()
        self.item_dao = StocktakingItemDAO()
        self.inventory_dao = InventoryDAO()
        self.stock_dao = StockLogDAO()

    # ============================================================
    # 创建盘点单
    # ============================================================
    def create_stocktaking(self, db: Session, order_in: StocktakingOrderCreate, user_id: int):
        """
        创建盘点单：
          - 读取商品当前库存数量（系统数量）
          - 保存盘点主单 + 明细数据
        """
        try:
            order_no = generate_stocktaking_no()
            order = StocktakingOrder(
                order_no=order_no,
                warehouse_id=order_in.warehouse_id,
                created_by=user_id,
                remark=order_in.remark,
            )
            db.add(order)
            db.flush()

            for item in order_in.items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if not product:
                    raise ValueError(f"商品ID {item.product_id} 不存在")

                inv = self.inventory_dao.get_by_product_warehouse(
                    db, item.product_id, order_in.warehouse_id
                )
                system_qty = inv.quantity if inv else 0
                diff_qty = item.counted_qty - system_qty

                item_obj = StocktakingItem(
                    stocktaking_id=order.id,
                    product_id=item.product_id,
                    system_qty=system_qty,
                    counted_qty=item.counted_qty,
                    diff_qty=diff_qty,
                    remark=item.remark,
                )
                db.add(item_obj)

            db.commit()
            db.refresh(order)
            return order

        except Exception as e:
            db.rollback()
            raise e

    # ============================================================
    # 确认盘点
    # ============================================================
    def confirm_stocktaking(self, db: Session, stocktaking_id: int, user_id: int):
        """
        确认盘点结果：
          - 状态流转：created → confirmed
          - 调整库存（根据差异数量）
          - 写入库存日志（StockAction.ADJUST）+ 记录当前操作人
        """
        order = self.order_dao.get(db, stocktaking_id)
        if not order:
            raise ValueError("盘点单不存在")
        if order.status != "created":
            raise ValueError("盘点单状态不可确认")

        items = self.item_dao.list_by_order(db, stocktaking_id)

        for item in items:
            inv = self.inventory_dao.get_by_product_warehouse(
                db, item.product_id, order.warehouse_id
            )
            # 若库存不存在则新建记录
            if not inv:
                inv = self.inventory_dao.create(
                    db,
                    {
                        "product_id": item.product_id,
                        "warehouse_id": order.warehouse_id,
                        "quantity": 0,
                    },
                )

            # 计算差异并调整库存
            diff = item.diff_qty
            if diff != 0:
                inv.quantity += diff
                db.commit()
                self.stock_dao.create(
                    db,
                    {
                        "inventory_id": inv.id,
                        "user_id": user_id,
                        "action": StockAction.ADJUST,
                        "change_qty": diff,
                        "remark": f"盘点调整 - {order.order_no}",
                    },
                )

        order.status = "confirmed"
        order.confirmed_by = user_id
        order.updated_at = datetime.now()
        db.commit()
        db.refresh(order)
        return order

    # ============================================================
    # 查询盘点列表
    # ============================================================
    def list_stocktakings(self, db: Session, user_id: int):
        """查询当前用户创建的盘点单"""
        return self.order_dao.list_orders(db, created_by=user_id)
