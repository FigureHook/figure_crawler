from sqlalchemy import Column, String

from src.database import PkModel


class Company(PkModel):
    __tablename__ = "company"

    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return self.name
