from sqlalchemy import Column, String

from src.database import PkModel


class Category(PkModel):
    __tablename__ = "category"

    name = Column(String, nullable=False, unique=True)
