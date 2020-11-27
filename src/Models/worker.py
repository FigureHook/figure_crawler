from sqlalchemy import Column, String, Integer
from src.database import Base


class Paintwork(Base):
    __tablename__ = "paintwork"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Sculptor(Base):
    __tablename__ = "sculptor"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
