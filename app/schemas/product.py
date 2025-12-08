"""
@ coding : utf-8 
@Time    : 2025/10/25 15:45
@Author  : admin
@Project : fastapi_wms
@File    : product.py
@Software: PyCharm
@Notes   : DTO-商品数据模型
"""
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """
    创建商品请求体：
        name : 商品名称。
        sku : 商品SKU编号。
        price : 商品价格。
        description : 商品描述（可选）。
    """
    name: str = Field(..., min_length=2, max_length=100, description="商品名称")
    sku: str = Field(..., min_length=2, max_length=50, description="商品SKU")
    price: float = Field(..., gt=0, description="商品价格")
    description: Optional[str] = Field(None, max_length=255, description="商品描述")

class ProductInfo(BaseModel):
    """
    商品信息响应体：
        id : 商品ID。
        name : 商品名称。
        sku : 商品SKU编号。
        price : 商品价格。
        description : 商品描述。
        is_active : 是否启用。
    """
    id: int
    name: str
    sku: str
    price: float
    description: Optional[str] = None
    is_active: bool

    model_config = {
        "from_attributes": True
    }
