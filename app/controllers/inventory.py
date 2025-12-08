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
    """
    创建库存记录
    :param inv_in:
        inv_in.product_id : 商品ID
        inv_in.warehouse_id : 仓库ID
        inv_in.quantity : 初始库存数量
    :param db:  数据库会话
    :param current_user: 当前登录用户
    :return: 新建库存记录信息
    """
    inv = inventory_service.create_inventory(db, inv_in)
    return ResponseModel(data=inv)

@rt_inventory.post("/{inv_id}/update", response_model=ResponseModel[InventoryInfo])
def update_inventory(
        inv_id: int,
        inv_update: InventoryUpdate,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    修改库存数量
    :param inv_id: 库存记录ID
    :param inv_update: 更新后的库存数量
    :param db: 数据库会话
    :param current_user: 当前登录用户
    :return: 修改后的库存信息
    """
    inv = inventory_service.update_quantity(db, inv_id, inv_update)
    return ResponseModel(data=inv)

@rt_inventory.get("/product/{product_id}", response_model=ResponseModel[List[InventoryInfo]])
def list_inventory_by_product(
        product_id: int,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    按商品ID查询库存
    :param product_id: 商品ID
    :param db: 数据库会话
    :param current_user:
    :return: 该商品在各仓库的库存列表 当前登录用户
    """
    data = inventory_service.list_by_product(db, product_id)
    return ResponseModel(data=data)

@rt_inventory.get("/warehouse/{warehouse_id}", response_model=ResponseModel[List[InventoryInfo]])
def list_inventory_by_warehouse(
        warehouse_id: int,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    按仓库ID查询库存
    :param warehouse_id: 仓库ID
    :param db:
    :param current_user:
    :return: 该仓库下所有商品的库存信息
    """
    data = inventory_service.list_by_warehouse(db, warehouse_id)
    return ResponseModel(data=data)
