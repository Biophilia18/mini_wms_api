"""
@ coding : utf-8
@Time    : 2025/12/10 00:18
@Author  : admin1
@Project : fastapi_wms
@File    : transfer.py
@Desc    :
@Notes   : 调拨模块接口控制层（Controller）
"""
import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.transfer import (
    TransferOrderCreate,
    TransferOrderUpdate,
    TransferOrderInfo,
)
from app.services.transfer_service import TransferService
from app.models.user import User


# ============================================================
# 路由初始化
# ============================================================
rt_transfer = APIRouter(prefix="/transfer", tags=["调拨管理"])
service = TransferService()


# ============================================================
# 创建调拨单
# ============================================================
@rt_transfer.post("/create", response_model=ResponseModel[TransferOrderInfo])
def create_transfer(
    order_in: TransferOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建调拨单接口：
      - 自动生成调拨单号
      - 插入主表 + 明细表
      - 初始状态为 created
    """
    try:
        order = service.create_transfer(db, order_in, current_user.id)
        return ResponseModel(data=order)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# 更新调拨单状态（审批/执行/确认）
# ============================================================
@rt_transfer.post("/{transfer_id}/status", response_model=ResponseModel[TransferOrderInfo])
def update_status(
    transfer_id: int,
    status_in: TransferOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新调拨单状态：
      - created → approved → executed → confirmed
      - 非法流转将返回 400 错误
    """
    try:
        order = service.update_status(db, transfer_id, status_in)
        return ResponseModel(data=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 执行调拨操作（仓间库存调整）
# ============================================================
@rt_transfer.post("/{transfer_id}/execute", response_model=ResponseModel[TransferOrderInfo])
def execute_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    执行调拨接口：
      - 检查状态是否 approved
      - 校验库存是否足够
      - 扣减调出仓库存 + 增加调入仓库存
      - 写入库存日志（StockAction.TRANSFER）
      - 更新状态为 executed
    """
    try:
        order = service.execute_transfer(db, transfer_id, current_user.id)
        return ResponseModel(data=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
        print("执行出错：->",e)
        traceback.print_exc()
        raise e

# ============================================================
# 查询调拨单列表
# ============================================================
@rt_transfer.get("/list", response_model=ResponseModel[list[TransferOrderInfo]])
def list_transfers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    查询当前用户创建的所有调拨单（按时间倒序）。
    """
    try:
        orders = service.list_transfers(db, current_user.id)
        return ResponseModel(data=orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
