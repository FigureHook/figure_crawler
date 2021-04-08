from sqlalchemy import Column, String

from src.database import PkModel, UniqueMixin

__all__ = [
    "Paintwork",
    "Sculptor"
]


class WorkerMultipleUniqueMixin(UniqueMixin):
    @classmethod
    def multiple_as_unique(cls, worker_names: list[str]) -> list:
        workers = []

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
