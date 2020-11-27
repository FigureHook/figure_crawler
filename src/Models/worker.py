from sqlalchemy import Column, String
from src.database import PkModel


class Paintwork(PkModel):
    __tablename__ = "paintwork"

    name = Column(String, nullable=False)


class Sculptor(PkModel):
    __tablename__ = "sculptor"

    name = Column(String, nullable=False)
