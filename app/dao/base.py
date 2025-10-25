"""
@ coding : utf-8 
@Time    : 2025/10/25 09:59
@Author  : admin
@Project : fastapi_wms
@File    : base.py
@Software: PyCharm
@Notes   : 抽象数据访问层
    作用：
      - 提供所有 DAO 通用的 CRUD 操作
      - 子类只需要指定 model，即可获得基础数据库功能
      - 避免重复写常规增删改查代码
"""
from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session

# 声明一个泛型类型变量 - 模型类型
ModelType = TypeVar("ModelType")


class BaseDAO(Generic[ModelType]):
    """
    通用抽象DAO基类
    子类记成时需传入具体orm模型，如BaseDAO(User)
    """

    def __init__(self, model: Type[ModelType]):
        """
        :param model: ORM模型类如User, Order等
        """
        self.model = model

    # 通用查询 read
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """根据主键id查询单条记录"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """查询所有记录，支持分页"""
        return db.query(self.model).offset(skip).limit(limit).all()

    # 创建 create
    def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """新增记录, 字典形式传入数据"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # 更新 update
    def update(self, db: Session, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """更新指定对象的字段"""
        for field, value in obj_in.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # 删除 delete
    def delete(self, db: Session, id: int)-> bool:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True

