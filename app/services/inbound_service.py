"""
@ coding : utf-8 
@Time    : 2025/12/8 21:12
@Author  : admin1
@Project : fastapi_wms
@File    : inbound_service.py
@Desc    :
@Notes   : 入库业务逻辑
"""
import datetime

from sqlalchemy.orm import Session

from app.dao.inbound_dao import InboundOrderDAO, InboundItemDAO
from app.dao.inventory_dao import InventoryDAO
from app.dao.stock_log_dao import StockLogDAO
from app.middleware.exceptions import AppException
from app.models.inbound_order import InboundOrder
from app.models.stock_log import StockAction
from app.schemas.base import ErrorCode
from app.schemas.inbound import InboundOrderCreate, InboundOrderUpdate


class InboundService:
    def __init__(self):
        self.inbound_dao = InboundOrderDAO()
        self.item_dao = InboundItemDAO()
        self.inventory_dao = InventoryDAO()
        self.stock_dao = StockLogDAO()

    # 入库单创建
    def create_inbound_order(self, db: Session, inbound_in: InboundOrderCreate, user_id: int) -> InboundOrder:
        """创建入库单及其明细"""
        order_no = self._generate_order_no() # 自动生成单号
        order_data = {
            "order_no": order_no,
            "warehouse_id": inbound_in.warehouse_id,
            "supplier": inbound_in.supplier,
            "created_by": user_id
        }
        new_order = self.inbound_dao.create(db, order_data)
        # 创建明细
        for item in inbound_in.items:
            item_data = {
                "inbound_id": new_order.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "remark": item.remark,
            }
            self.item_dao.create(db, item_data)
        return new_order

    # 状态流转
    def update_status(self, db: Session, inbound_id: int, update_in: InboundOrderUpdate):
        """更新入库单状态"""
        order = self.inbound_dao.get(db, inbound_id)
        if not order:
            raise  AppException(ErrorCode.PARAM_ERROR, "入库单不存在")
        valid_transitions = {
            "created":["approved"],
            "approved":["executed"],
            "executed":["confirmed"]
        }
        if update_in.status not in valid_transitions.get(order.status, []):
            raise  AppException(ErrorCode.PARAM_ERROR,f"非法状态流转:{order.status} -> {update_in.status}")
        order.status = update_in.status
        db.commit()
        db.refresh(order)
        return order

    # 入库执行，影响库存 日志
    def execute_inbound(self, db: Session, inbound_id: int, user_id: int):
        """执行入库"""
        order = self.inbound_dao.get(db, inbound_id)
        if not order:
            raise AppException(ErrorCode.PARAM_ERROR,"入库单不存在")
        if order.status != "approved":
            raise AppException(ErrorCode.PARAM_ERROR, f"当前状态不可执行入库：{order.status}")
        items = self.item_dao.list_by_inbound_id(db, inbound_id)
        if not items:
            raise AppException(ErrorCode.PARAM_ERROR, "入库明细为空")
        for item in items:
            inv = self.inventory_dao.get_by_product_warehouse(db, item.product_id, order.warehouse_id)
            if inv:
                inv.quantity += item.quantity
                db.commit()
            else:
                inv = self.inventory_dao.create(db,{
                    "product_id": item.product_id,
                    "warehouse_id": order.warehouse_id,
                    "quantity": item.quantity
                })
            # 写入库日志
            self.stock_dao.create(db, {
                "inventory_id": inv.id,
                "user_id": user_id,
                "action": StockAction.IN,
                "change_qty": item.quantity,
                "remark": f"入库单 - {order.order_no}"
            })

        # 修改状态为executed
        order.status = "executed"
        db.commit()
        db.refresh(order)
        return order

    def _generate_order_no(self):
        """生成软入库单号"""
        now = datetime.datetime.now()
        return f"IN{now.strftime('%Y%m%d%H%M%S')}"
