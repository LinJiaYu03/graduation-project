from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy.orm import Query, Session

from app.db.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """同步 SQLAlchemy Session 的通用 CRUD 基类。

    约定：repository 只负责数据访问，不提交事务；commit / rollback 由 service 控制。
    """

    def __init__(self, db: Session, model: Type[ModelT]) -> None:
        self.db = db
        self.model = model

    def get(self, pk: Any) -> Optional[ModelT]:
        """按主键取单条，不存在返回 None。"""
        return self.db.get(self.model, pk)

    def get_by(self, **filters: Any) -> Optional[ModelT]:
        """按字段等值条件取单条，不存在返回 None。"""
        return self.db.query(self.model).filter_by(**filters).first()

    def exists(self, **filters: Any) -> bool:
        """是否存在满足等值条件的记录。"""
        return self.get_by(**filters) is not None

    def count(self, **filters: Any) -> int:
        """统计满足等值条件的记录数；不传条件时统计全表。"""
        query = self.db.query(self.model)
        if filters:
            query = query.filter_by(**filters)
        return query.count()

    def paginate(
        self,
        page: int,
        page_size: int,
        order_by: Any = None,
        **filters: Any,
    ) -> tuple[int, list[ModelT]]:
        """分页查询，返回 (总数, 当前页记录)；order_by 为 None 时不排序。"""
        query = self.db.query(self.model)
        if filters:
            query = query.filter_by(**filters)
        return self.paginate_query(query, page, page_size, order_by)

    def paginate_query(
        self,
        query: Query,
        page: int,
        page_size: int,
        order_by: Any = None,
    ) -> tuple[int, list[ModelT]]:
        """对已构造的查询分页，返回 (总数, 当前页记录)。"""
        total = query.count()
        if order_by is not None:
            query = query.order_by(order_by)
        records = query.offset((page - 1) * page_size).limit(page_size).all()
        return total, records

    def create(self, **values: Any) -> ModelT:
        """新建并 flush 以拿到主键；不提交事务。"""
        instance = self.model(**values)
        self.db.add(instance)
        self.db.flush()
        return instance

    def update(self, instance: ModelT, **values: Any) -> ModelT:
        """部分字段更新，不 flush / commit。"""
        for field, value in values.items():
            setattr(instance, field, value)
        return instance

    def delete(self, instance: ModelT) -> None:
        """删除实例，不提交事务。"""
        self.db.delete(instance)
