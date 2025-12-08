"""
@ coding : utf-8 
@Time    : 2025/12/8 22:55
@Author  : admin1
@Project : fastapi_wms
@File    : outbound.py
@Desc    :
@Notes   : 出库模块接口控制层（Controller）
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.outbound import (
    OutboundOrderCreate,
    OutboundOrderUpdate,
    OutboundOrderInfo,
)
from app.services.outbound_service import OutboundService
from app.models.user import User  # 用户模型

# ============================================================
# 路由初始化
# ============================================================
rt_outbound = APIRouter(prefix="/outbound", tags=["出库管理"])
service = OutboundService()



@rt_outbound.post("/create", response_model=ResponseModel[OutboundOrderInfo])
def create_outbound(
    order_in: OutboundOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建出库单接口：
      - 自动生成出库单号
      - 插入主表 + 明细表
      - 初始状态为 created
    """
    try:
        order = service.create_outbound(db, order_in, current_user.id)
        return ResponseModel(data=order)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))



@rt_outbound.post("/{outbound_id}/status", response_model=ResponseModel[OutboundOrderInfo])
def update_status(
    outbound_id: int,
    status_in: OutboundOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新出库单状态：
      - created → approved → executed → confirmed
      - 非法流转将返回 400 错误
    """
    try:
        order = service.update_status(db, outbound_id, status_in)
        return ResponseModel(data=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@rt_outbound.post("/{outbound_id}/execute", response_model=ResponseModel[OutboundOrderInfo])
def execute_outbound(
    outbound_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    执行出库接口：
      - 检查状态是否 approved
      - 校验库存是否足够
      - 扣减库存数量
      - 写入库存日志（StockAction.OUT）
      - 更新单据状态为 executed
    """
    try:
        order = service.execute_outbound(db, outbound_id, current_user.id)
        return ResponseModel(data=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@rt_outbound.get("/list", response_model=ResponseModel[list[OutboundOrderInfo]])
def list_outbounds(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取当前用户创建的所有出库单（按时间倒序）。
    """
    try:
        orders = service.list_outbounds(db, current_user.id)
        return ResponseModel(data=orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
