"""
@ coding : utf-8 
@Time    : 2025/10/26 09:51
@Author  : admin
@Project : fastapi_wms
@File    : inventory.py
@Software: PyCharm
@Notes   : 库存相关接口
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.inventory import InventoryInfo, InventoryCreate, InventoryUpdate
from app.services.inventory_service import InventoryService

rt_inventory = APIRouter(prefix="/inventory", tags=["inventory"])
inventory_service = InventoryService()

@rt_inventory.post("/create", response_model=ResponseModel[InventoryInfo])
def create_inventory(
        inv_in: InventoryCreate,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """创建库存记录"""
    inv = inventory_service.create_inventory(db, inv_in)
    return ResponseModel(data=inv)

@rt_inventory.post("/{inv_id}/update", response_model=ResponseModel[InventoryInfo])
def update_inventory(
        inv_id: int,
        inv_update: InventoryUpdate,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """修改库存数量"""
    inv = inventory_service.update_quantity(db, inv_id, inv_update)
    return ResponseModel(data=inv)

@rt_inventory.get("/product/{product_id}", response_model=ResponseModel[List[InventoryInfo]])
def list_inventory_by_product(
        product_id: int,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """查询某商品的所有库存"""
    data = inventory_service.list_by_product(db, product_id)
    return ResponseModel(data=data)

@rt_inventory.get("/warehouse/{warehouse_id}", response_model=ResponseModel[List[InventoryInfo]])
def list_inventory_by_warehouse(
        warehouse_id: int,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """查询某仓库的的所有商品库存"""
    data = inventory_service.list_by_warehouse(db, warehouse_id)
    return ResponseModel(data=data)
