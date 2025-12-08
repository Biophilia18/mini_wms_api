"""
@ coding : utf-8 
@Time    : 2025/12/8 21:35
@Author  : admin1
@Project : fastapi_wms
@File    : inbound.py
@Desc    :
@Notes   :  入库单接口控制层
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.inbound import InboundOrderInfo, InboundOrderCreate, InboundOrderUpdate
from app.services.inbound_service import InboundService

rt_inbound = APIRouter(prefix="/inbound", tags=["inbound, 入库模块"])
inbound_service = InboundService()

@rt_inbound.post("/create", response_model=ResponseModel[InboundOrderInfo])
def create_inbound(
        inbound_in: InboundOrderCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """创建入库单"""
    new_order = inbound_service.create_inbound_order(db, inbound_in, current_user.id)
    return ResponseModel(data=new_order)

@rt_inbound.post("/{inbound_id}/status", response_model=ResponseModel[InboundOrderInfo])
def update_status(
        inbound_id: int,
        update_in: InboundOrderUpdate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """更新入库单状态:审批 执行 确认"""
    update_order = inbound_service.update_status(db, inbound_id, update_in)
    return ResponseModel(data=update_order)

@rt_inbound.post("/{inbound_id}/execute", response_model=ResponseModel[InboundOrderInfo])
def execute_inbound(
        inbound_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """执行入库操作 更新库存和日志记录"""
    executed_order = inbound_service.execute_inbound(db, inbound_id, current_user.id)
    return ResponseModel(data=executed_order)

@rt_inbound.get('/list', response_model=ResponseModel[List[InboundOrderInfo]])
def list_inbound(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """查询当前用户创建的入库单"""
    data = inbound_service.inbound_dao.list_by_user(db, current_user.id)
    return ResponseModel(data=data)
