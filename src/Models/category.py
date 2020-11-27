from sqlalchemy import Column, String, Integer

from src.database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
