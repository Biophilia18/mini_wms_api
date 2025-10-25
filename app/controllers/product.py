"""
@ coding : utf-8 
@Time    : 2025/10/25 15:56
@Author  : admin
@Project : fastapi_wms
@File    : product.py
@Software: PyCharm
@Notes   : 商品接口层
"""
from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.base import ResponseModel
from app.schemas.product import ProductInfo, ProductCreate
from app.services.product_service import ProductService

rt_product = APIRouter(prefix="/product", tags=["product,商品接口列表"])
product_service = ProductService()


@rt_product.post("/create", response_model=ResponseModel[ProductInfo])
def create_product(
        product_in: ProductCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)  # 登录保护
):
    new_product = product_service.create_product(db, product_in)
    return ResponseModel(data=new_product)


@rt_product.get("/list", response_model=ResponseModel[List[ProductInfo]])
def list_products(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    products = product_service.list_products(db)
    return ResponseModel(data=products)


