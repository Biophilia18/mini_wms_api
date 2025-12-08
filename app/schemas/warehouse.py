"""
@ coding : utf-8 
@Time    : 2025/10/25 17:33
@Author  : admin
@Project : fastapi_wms
@File    : warehouse.py
@Software: PyCharm
@Notes   : 仓库数据模型，定义接口数据格式和验证规则
"""
from typing import Optional

from pydantic import BaseModel, Field


class WarehouseCreate(BaseModel):
    """
    创建仓库请求体：
        name : 仓库名称。
        code : 仓库编码。
        address : 仓库地址（可选）。
        capacity : 仓库容量（可选，大于0）。
        manager_id : 管理员用户ID。
    """
    name: str = Field(..., min_length=2, max_length=100, description="仓库名称")
    code: str = Field(..., min_length=2, max_length=20, description="仓库编码")
    address: Optional[str] = Field(None, max_length=200, description="仓库地址")
    capacity: Optional[int] = Field(None, gt=0, description="仓库容量")
    manager_id: int = Field(..., gt=0, description="管理员用户id")

class WarehouseInfo(BaseModel):
    """
    仓库信息响应体：
        id : 仓库ID。
        name : 仓库名称。
        code : 仓库编码。
        address : 仓库地址。
        capacity : 仓库容量。
        manager_id : 管理员用户ID。
        is_active : 是否启用。
    """
    id: int
    name: str
    code: str
    address: Optional[str]
    capacity: Optional[int]
    manager_id: int
    is_active: bool
    model_config = {
        "from_attributes": True
    }
