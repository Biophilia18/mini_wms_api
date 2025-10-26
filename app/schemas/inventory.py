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
    product_id: int = Field(..., gt=0,description="商品id") # id>0
    warehouse_id: int = Field(..., gt=0, description="仓库id")
    quantity: int = Field(...,ge=0, description="初始库存数量")# 不能为负数
class InventoryUpdate(BaseModel):
    quantity:int = Field(..., ge=0, description="新的库存数量")

class InventoryInfo(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    quantity: int

    model_config = {
        "from_attributes": True
    }