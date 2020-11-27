from sqlalchemy import Column, String, Integer

from src.database import Base


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return self.name


class Manufacturer(Base):
    __tablename__ = "manufacturer"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
