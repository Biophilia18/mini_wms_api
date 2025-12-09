"""
@ coding : utf-8 
@Time    : 2025/12/9 10:56
@Author  : admin1
@Project : fastapi_wms
@File    : serializer.py
@Desc    :
@Notes   : 统一 ORM -> Pydantic Schema 序列化工具
"""

from typing import List, Type, TypeVar, Any
from pydantic import BaseModel

# 泛型类型：用于标注目标 Schema 类型
SchemaType = TypeVar("SchemaType", bound=BaseModel)


def to_schema(schema_cls: Type[SchemaType], orm_obj: Any) -> SchemaType | None:
    """
    将单个 ORM 对象转换为指定 Schema 实例
    :param schema_cls: 目标 Pydantic Schema 类
    :param orm_obj: ORM 实例
    :return: Schema 实例
    """
    if orm_obj is None:
        return None
    return schema_cls.model_validate(orm_obj)


def to_schema_list(schema_cls: Type[SchemaType], orm_list: List[Any]) -> List[SchemaType]:
    """
    将 ORM 对象列表转换为 Schema 实例列表
    :param schema_cls: 目标 Pydantic Schema 类
    :param orm_list: ORM 对象列表
    :return: Schema 实例列表
    """
    if not orm_list:
        return []
    return [schema_cls.model_validate(obj) for obj in orm_list]
