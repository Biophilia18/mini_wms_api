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
from app.services.warehouse_service import WarehouseService

rt_warehouse = APIRouter(prefix="/warehouse", tags=["warehouse,仓库接口"])
warehouse_service = WarehouseService()

@rt_warehouse.post("/create",response_model=ResponseModel[WarehouseInfo])
def create_warehouse(
        warehouse_in: WarehouseCreate,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    创建新仓库
    :param warehouse_in:
        warehouse_in.name : 仓库名称
        warehouse_in.code : 仓库编码
        warehouse_in.address : 仓库地址
        warehouse_in.capacity : 仓库容量
        warehouse_in.manager_id : 管理员用户ID
    :param db: 数据库会话
    :param current_user: 当前登录用户
    :return: 新建仓库信息
    """
    new_warehouse = warehouse_service.create_warehouse(db,warehouse_in)
    return ResponseModel(data=new_warehouse)

@rt_warehouse.get("/list",response_model=ResponseModel[List[WarehouseInfo]])
def list_warehouses(
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    查询所有仓库
    :param db: 数据库会话
    :param current_user: 当前登录用户
    :return: 仓库信息列表
    """
    warehouses = warehouse_service.list_warehouses(db)
    return ResponseModel(data=warehouses)

@rt_warehouse.post("/{warehouse_id}/toggle_status",response_model=ResponseModel[WarehouseInfo])
def toggle_warehouse_status(
        warehouse_id: int,
        db: Session=Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    根据仓库id切换使用、禁用状态
    :param warehouse_id: 仓库ID
    :param db: 数据库会话
    :param current_user: 当前登录用户
    :return: 更新后的仓库信息
    """
    warehouse = warehouse_service.toggle_warehouse_status(db,warehouse_id)
    return ResponseModel(data=warehouse)

