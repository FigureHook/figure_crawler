from typing import List, Type, TypeVar, Optional

from sqlalchemy import Column, String

from .base import PkModel, UniqueMixin

__all__ = [
    "Paintwork",
    "Sculptor"
]

U = TypeVar('U', bound='UniqueMixin')


class WorkerMultipleUniqueMixin(UniqueMixin):
    __abstract__ = True

    @classmethod
    def multiple_as_unique(cls: Type[U], worker_names: List[str]) -> List[Optional[U]]:
        workers: List[Optional[U]] = []
        for name in worker_names:
            worker = cls.as_unique(name=name)
            workers.append(worker)

        return workers


class Paintwork(WorkerMultipleUniqueMixin, PkModel):
    __tablename__ = "paintwork"

    name = Column(String, nullable=False)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Paintwork.name == name)


class Sculptor(WorkerMultipleUniqueMixin, PkModel):
    __tablename__ = "sculptor"

    name = Column(String, nullable=False)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Sculptor.name == name)
