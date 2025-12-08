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
    """
    创建商品信息
    :param product_in:
        product_in.name : 商品名称
        product_in.sku : 商品SKU编号
        product_in.price : 商品单价
        product_in.description : 商品描述
    :param db: 数据库会话
    :param current_user: 当前登录用户
    :return: 新增商品的完整信息
    """
    new_product = product_service.create_product(db, product_in)
    return ResponseModel(data=new_product)


@rt_product.get("/list", response_model=ResponseModel[List[ProductInfo]])
def list_products(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    获取商品列表
    :param db: 数据库会话
    :param current_user: 当前登录用户
    :return: 所有商品的基本信息列表
    """
    products = product_service.list_products(db)
    return ResponseModel(data=products)


