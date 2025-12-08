"""
@ coding : utf-8 
@Time    : 2025/10/26 09:25
@Author  : admin
@Project : fastapi_wms
@File    : inventory.py
@Software: PyCharm
@Notes   :
"""
from pydantic import BaseModel, Field


class InventoryCreate(BaseModel):
    """
    创建库存记录请求体：
        product_id : 商品ID，必须大于0。
        warehouse_id : 仓库ID，必须大于0。
    """
    product_id: int = Field(..., gt=0,description="商品id") # id>0
    warehouse_id: int = Field(..., gt=0, description="仓库id")
    quantity: int = Field(...,ge=0, description="初始库存数量")# 不能为负数

class InventoryUpdate(BaseModel):
    """
    更新库存数量请求体：
        quantity : 新的库存数量，非负数。
    """
    quantity:int = Field(..., ge=0, description="新的库存数量")

class InventoryInfo(BaseModel):
    """
    库存信息响应体：
        id : 库存记录ID。
        product_id : 商品ID。
        warehouse_id : 仓库ID。
        quantity : 当前库存数量。
    """
    id: int
    product_id: int
    warehouse_id: int
    quantity: int

    model_config = {
        "from_attributes": True
    }
