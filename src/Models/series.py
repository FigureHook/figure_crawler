from sqlalchemy import Column, String, Integer

from src.database import Base


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
