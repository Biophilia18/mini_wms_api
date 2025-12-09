"""
@ coding : utf-8 
@Time    : 2025/12/9 17:44
@Author  : admin1
@Project : fastapi_wms
@File    : stocktaking.py
@Desc    :
@Notes   : 盘点模块接口控制层（Controller）
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.stocktaking import (
    StocktakingOrderCreate,
    StocktakingOrderInfo,
)
from app.services.stocktaking_service import StocktakingService
from app.models.user import User

# ============================================================
# 路由初始化
# ============================================================
rt_stocktaking = APIRouter(prefix="/stocktaking", tags=["库存盘点"])
service = StocktakingService()


# ============================================================
# 创建盘点单
# ============================================================
@rt_stocktaking.post("/create", response_model=ResponseModel[StocktakingOrderInfo])
def create_stocktaking(
        order_in: StocktakingOrderCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    创建盘点单接口：
      - 自动生成盘点单号
      - 记录系统数量与实盘数量
      - 计算差异数量（counted_qty - system_qty）
    """
    try:
        order = service.create_stocktaking(db, order_in, current_user.id)
        return ResponseModel(data=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 确认盘点结果
# ============================================================
@rt_stocktaking.post("/{stocktaking_id}/confirm", response_model=ResponseModel[StocktakingOrderInfo])
def confirm_stocktaking(
        stocktaking_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    确认盘点接口：
      - 自动识别当前用户为确认人
      - 调整库存 + 写入日志 + 更新状态
    """
    try:
        order = service.confirm_stocktaking(db, stocktaking_id, current_user.id)
        return ResponseModel(data=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 查询盘点单列表
# ============================================================
@rt_stocktaking.get("/list", response_model=ResponseModel[list[StocktakingOrderInfo]])
def list_stocktakings(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    获取当前用户创建的所有盘点单（按时间倒序）。
    """
    try:
        orders = service.list_stocktakings(db, current_user.id)
        return ResponseModel(data=orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 查询盘点单详情
# ============================================================
@rt_stocktaking.get("/{stocktaking_id}", response_model=ResponseModel[StocktakingOrderInfo])
def get_stocktaking_detail(
        stocktaking_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    获取盘点单详情：
      - 包含主单信息 + 明细行
    """
    try:
        order = service.order_dao.get(db, stocktaking_id)
        if not order:
            raise HTTPException(status_code=404, detail="盘点单不存在")
        return ResponseModel(data=order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
