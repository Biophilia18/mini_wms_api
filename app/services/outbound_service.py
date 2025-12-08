"""
@ coding : utf-8 
@Time    : 2025/12/8 22:49
@Author  : admin1
@Project : fastapi_wms
@File    : outbound_service.py
@Desc    :
@Notes   : 
"""
from app.dao.outbound import OutboundOrderDAO, OutboundItemDAO
from app.dao.stock_log_dao import StockLogDAO
from app.models.product import Product
from app.models.stock_log import StockAction

"""
@ coding : utf-8
@Time    : 2025/12/08 23:10
@Author  : admin
@Project : fastapi_wms
@File    : outbound_service.py
@Software: PyCharm
@Notes   : 出库业务逻辑层（Service）
"""

from datetime import datetime
from sqlalchemy.orm import Session

from app.dao.inventory_dao import InventoryDAO
from app.models.outbound import OutboundOrder, OutboundItem
from app.schemas.outbound import OutboundOrderCreate, OutboundOrderUpdate


def generate_outbound_order_no():
    """生成出库单号"""
    now = datetime.now()
    return f"OUT{now.strftime('%Y%m%d%H%M%S')}"


class OutboundService:
    """
    出库业务逻辑类：
      - 封装出库模块核心流程
      - 包含：创建出库单、状态流转、执行出库（扣减库存 + 写日志）、列表查询
    """

    def __init__(self):
        self.outbound_order_dao = OutboundOrderDAO()
        self.outbound_item_dao = OutboundItemDAO()
        self.inventory_dao = InventoryDAO()
        self.stock_dao = StockLogDAO()

    # ============================================================
    # 出库单创建
    # ============================================================
    def create_outbound(self, db: Session, order_in: OutboundOrderCreate, user_id: int):
        """
        创建出库单及明细:
          - 校验商品是否存在
          - 创建出库主表与明细记录
        """
        try:
            # 校验所有商品ID有效性
            for item in order_in.items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if not product:
                    raise ValueError(f"商品ID {item.product_id} 不存在")

            # 生成出库单号
            order_no = "OUT" + datetime.now().strftime("%Y%m%d%H%M%S")

            # 创建主单对象
            order = OutboundOrder(
                order_no=order_no,
                warehouse_id=order_in.warehouse_id,
                customer=order_in.customer,
                outbound_type=order_in.outbound_type,
                created_by=user_id,
            )
            db.add(order)
            db.flush()  # 立即生成 order.id

            # 添加明细行
            for item in order_in.items:
                item_obj = OutboundItem(
                    outbound_id=order.id,
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
            raise e  # 直接抛出业务错误
        except Exception as e:
            db.rollback()
            print("创建出库单失败:", e)
            raise e

    # ============================================================
    # 状态流转
    # ============================================================
    def update_status(self, db: Session, outbound_id: int, status_in: OutboundOrderUpdate):
        """
        更新出库单状态。
        :param db: 数据库会话
        :param outbound_id: 出库单ID
        :param status_in: 出库单状态更新对象（OutboundOrderUpdate）
        :return: 更新后的出库单 ORM 对象
        """
        order = self.outbound_order_dao.get(db, outbound_id)
        if not order:
            raise ValueError("出库单不存在")

        # 校验合法的状态流转
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
    # 执行出库
    # ============================================================
    def execute_outbound(self, db: Session, outbound_id: int, user_id: int):
        """
        执行出库操作。
        :param db: 数据库会话
        :param outbound_id: 出库单ID
        :param user_id: 当前操作用户ID
        :return: 执行后的出库单 ORM 对象
        """
        order = self.outbound_order_dao.get(db, outbound_id)
        if not order:
            raise ValueError("出库单不存在")
        if order.status != "approved":
            raise ValueError("当前状态不可执行出库")

        # 查询明细
        items = self.outbound_item_dao.get_by_outbound_id(db, outbound_id)

        # 遍历每个出库行，校验库存是否足够
        for item in items:
            inv = self.inventory_dao.get_by_product_warehouse(
                db, item.product_id, order.warehouse_id
            )
            if not inv:
                raise ValueError(f"商品ID {item.product_id} 无库存记录，无法出库")
            if inv.quantity < item.quantity:
                raise ValueError(
                    f"商品ID {item.product_id} 库存不足：当前 {inv.quantity}，出库 {item.quantity}"
                )

        # 统一扣减库存 + 写日志
        for item in items:
            inv = self.inventory_dao.get_by_product_warehouse(
                db, item.product_id, order.warehouse_id
            )
            inv.quantity -= item.quantity
            db.commit()

            # 写库存日志
            self.stock_dao.create(
                db,
                {
                    "inventory_id": inv.id,
                    "user_id": user_id,
                    "action": StockAction.OUT,
                    "change_qty": -item.quantity,  # 出库为负
                    "remark": f"出库单 - {order.order_no}",
                },
            )

        # 更新单据状态
        order.status = "executed"
        order.updated_at = datetime.now()
        db.commit()
        db.refresh(order)

        return order

    # ============================================================
    # 查询出库单列表
    # ============================================================
    def list_outbounds(self, db: Session, user_id: int):
        """
        查询当前用户创建的所有出库单（按时间倒序）。
        :param db: 数据库会话
        :param user_id: 当前登录用户ID
        :return: 出库单对象列表
        """
        return self.outbound_order_dao.get_by_user(db, user_id)
