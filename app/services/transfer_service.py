"""
@ coding : utf-8
@Time    : 2025/12/09 23:50
@Author  : admin1
@Project : fastapi_wms
@File    : transfer_service.py
@Desc    :
@Notes   : 调拨模块业务逻辑层（Service）
"""

from datetime import datetime
from sqlalchemy.orm import Session

from app.dao.inventory_dao import InventoryDAO
from app.dao.stock_log_dao import StockLogDAO
from app.dao.transfer_dao import TransferOrderDAO, TransferItemDAO
from app.models.transfer import TransferOrder, TransferItem
from app.models.product import Product
from app.models.stock_log import StockAction
from app.schemas.transfer import TransferOrderCreate, TransferOrderUpdate


def generate_transfer_no():
    """生成调拨单号"""
    now = datetime.now()
    return f"TRF{now.strftime('%Y%m%d%H%M%S')}"


class TransferService:
    """
    调拨业务逻辑类：
      - 封装调拨模块核心流程
      - 包含：创建调拨单、状态流转、执行调拨（仓间移库）、列表查询
    """

    def __init__(self):
        self.transfer_order_dao = TransferOrderDAO()
        self.transfer_item_dao = TransferItemDAO()
        self.inventory_dao = InventoryDAO()
        self.stock_dao = StockLogDAO()

    # ============================================================
    # 创建调拨单
    # ============================================================
    def create_transfer(self, db: Session, order_in: TransferOrderCreate, user_id: int):
        """
        创建调拨单及明细：
          - 校验商品是否存在
          - 创建调拨主表与明细记录
        """
        try:
            for item in order_in.items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if not product:
                    raise ValueError(f"商品ID {item.product_id} 不存在")

            transfer_no = generate_transfer_no()
            order = TransferOrder(
                transfer_no=transfer_no,
                source_warehouse_id=order_in.source_warehouse_id,
                target_warehouse_id=order_in.target_warehouse_id,
                remark=order_in.remark,
                created_by=user_id,
            )
            db.add(order)
            db.flush()

            for item in order_in.items:
                item_obj = TransferItem(
                    transfer_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    remark=item.remark,
                )
                db.add(item_obj)

            db.commit()
            db.refresh(order)
            return order

        except ValueError as e:
            db.rollback()
            raise e
        except Exception as e:
            db.rollback()
            print("创建调拨单失败:", e)
            raise e

    # ============================================================
    # 状态流转（审批/执行/确认）
    # ============================================================
    def update_status(self, db: Session, transfer_id: int, status_in: TransferOrderUpdate):
        """
        更新调拨单状态：
          - created → approved → executed → confirmed
        """
        order = self.transfer_order_dao.get(db, transfer_id)
        if not order:
            raise ValueError("调拨单不存在")

        valid_flow = {
            "created": ["approved"],
            "approved": ["executed"],
            "executed": ["confirmed"],
        }
        if status_in.status not in valid_flow.get(order.status, []):
            raise ValueError(f"非法状态流转：{order.status} → {status_in.status}")

        order.status = status_in.status
        db.commit()
        db.refresh(order)
        return order

    # ============================================================
    # 执行调拨
    # ============================================================
    def execute_transfer(self, db: Session, transfer_id: int, user_id: int):
        """
        执行调拨操作：
          - 检查状态是否 approved
          - 校验调出仓库存是否足够
          - 扣减调出仓库存 + 增加调入仓库存
          - 写入库存日志（StockAction.TRANSFER）
        """
        order = self.transfer_order_dao.get(db, transfer_id)
        if not order:
            raise ValueError("调拨单不存在")
        if order.status != "approved":
            raise ValueError("当前状态不可执行调拨")

        items = self.transfer_item_dao.get_by_transfer_id(db, transfer_id)
        if not items:
            raise ValueError("调拨明细为空")

        # 校验库存
        for item in items:
            inv = self.inventory_dao.get_by_product_warehouse(
                db, item.product_id, order.source_warehouse_id
            )
            if not inv:
                raise ValueError(f"调出仓无库存记录，商品ID {item.product_id}")
            if inv.quantity < item.quantity:
                raise ValueError(
                    f"调出仓库存不足：商品 {item.product_id}，现有 {inv.quantity}，调拨 {item.quantity}"
                )

        # 扣减调出仓库存 & 增加调入仓库存
        for item in items:
            # 调出仓
            src_inv = self.inventory_dao.get_by_product_warehouse(
                db, item.product_id, order.source_warehouse_id
            )
            src_inv.quantity -= item.quantity
            db.commit()

            # 调入仓
            tgt_inv = self.inventory_dao.get_by_product_warehouse(
                db, item.product_id, order.target_warehouse_id
            )
            if tgt_inv:
                tgt_inv.quantity += item.quantity
            else:
                self.inventory_dao.create(
                    db,
                    {
                        "warehouse_id": order.target_warehouse_id,
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                    },
                )
            db.commit()

            # 写库存日志
            self.stock_dao.create(
                db,
                {
                    "inventory_id": src_inv.id,
                    "user_id": user_id,
                    "action": StockAction.TRANSFER,
                    "change_qty": -item.quantity,
                    "remark": f"调拨单 - {order.transfer_no} 调出仓扣减",
                },
            )

        order.status = "executed"
        order.updated_at = datetime.now()
        db.commit()
        db.refresh(order)
        return order

    # ============================================================
    # 查询调拨单列表
    # ============================================================
    def list_transfers(self, db: Session, user_id: int):
        """
        查询当前用户创建的所有调拨单（按时间倒序）
        """
        return self.transfer_order_dao.get_by_user(db, user_id)
