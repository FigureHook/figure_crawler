from .base import Model
from sqlalchemy import Column, Enum, DateTime
from sqlalchemy.sql import func
from ..constants import PeriodicTask

__all__ = [
    "Task"
]


class Task(Model):
    __tablename__ = "periodic_task"
    __datetime_callback__ = func.now

    name = Column(Enum(PeriodicTask), primary_key=True)
    executed_at = Column(
        DateTime,
        default=__datetime_callback__(),
        onupdate=__datetime_callback__()
    )

    def update(self):
        return super().update(executed_at=self.__datetime_callback__())
