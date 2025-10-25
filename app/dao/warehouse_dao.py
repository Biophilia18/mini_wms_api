"""
@ coding : utf-8 
@Time    : 2025/10/25 17:26
@Author  : admin
@Project : fastapi_wms
@File    : warehouse_dao.py
@Software: PyCharm
@Notes   :
    仓库数据访问对象
    继承BaseDAO获得基础CRUD，扩展仓库特有查询方法
"""
from sqlalchemy.orm import Session
from app.dao.base import BaseDAO
from app.models.warehouse import WareHouse


class WareHouseDAO(BaseDAO[WareHouse]):
    def __init__(self):
        super().__init__(WareHouse)

    def get_by_code(self, db: Session, code: str):
        """按仓库编码查询"""
        return db.query(WareHouse).filter(WareHouse.code == code).first()

    def get_by_name(self, db: Session, name: str):
        """按仓库名称查询"""
        return db.query(WareHouse).filter(WareHouse.name == name).first()

    def get_active_warehouses(self, db: Session):
        """获取所有启用的仓库"""
        return db.query(WareHouse).filter(WareHouse.is_active == True).all()

    def get_warehouse_by_manager(self, db: Session, manager_id: int):
        """获取指定管理员管理的仓库"""
        return db.query(WareHouse).filter(WareHouse.manager_id == manager_id).all()
