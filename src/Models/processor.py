from sqlalchemy import Column, DateTime, Enum
from sqlalchemy.sql import func

from ..constants import ProcessorID, ProcessorType, ProcessorStatus
from .base import Model

__all__ = [
    "ProcessorStatus"
]


class Processor(Model):
    __tablename__ = "processor"
    __datetime_callback__ = func.now

    name = Column(Enum(ProcessorID), primary_key=True)
    type_ = Column("type", Enum(ProcessorType), nullable=False)
    status = Column(Enum(ProcessorStatus))
    executed_at = Column(
        DateTime,
        default=__datetime_callback__(),
        onupdate=__datetime_callback__()
    )
