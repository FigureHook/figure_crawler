from sqlalchemy import Column, String

from src.database import PkModel


class Series(PkModel):
    __tablename__ = "series"

    name = Column(String, nullable=False, unique=True)
