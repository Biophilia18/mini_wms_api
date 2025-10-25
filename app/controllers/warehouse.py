"""
@ coding : utf-8 
@Time    : 2025/10/25 21:26
@Author  : admin
@Project : fastapi_wms
@File    : warehouse.py
@Software: PyCharm
@Notes   : 仓库接口配置
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.warehouse import WarehouseInfo, WarehouseCreate
from app.services.warehouse_service import WareHouseService

rt_warehouse = APIRouter(prefix="/warehouse", tags=["warehouse,仓库接口"])
warehouse_service = WareHouseService()

@rt_warehouse.post("/create",response_model=ResponseModel[WarehouseInfo])
def create_warehouse(
        warehouse_in: WarehouseCreate,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """创建新仓库"""
    new_warehouse = warehouse_service.create_warehouse(db,warehouse_in)
    return ResponseModel(data=new_warehouse)

@rt_warehouse.get("/list",response_model=ResponseModel[List[WarehouseInfo]])
def list_warehouses(
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """获取仓库列表"""
    warehouses = warehouse_service.list_warehouses(db)
    return ResponseModel(data=warehouses)

@rt_warehouse.post("/{warehouse_id}/toggle_status",response_model=ResponseModel[WarehouseInfo])
def toggle_warehouse_status(
        warehouse_id: int,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """根据仓库id切换使用、禁用状态"""
    warehouse = warehouse_service.toggle_warehouse_status(db,warehouse_id)
    return ResponseModel(data=warehouse)

