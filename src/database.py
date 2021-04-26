import os
from contextlib import contextmanager
from typing import ClassVar, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from .Models.base import Model

# https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session


class PostgreSQLDB:
    _instance = None

    _engine: ClassVar[Optional[Engine]] = None
    _Session = None

    def __new__(cls) -> 'PostgreSQLDB':
        if not cls._instance:
            if os.getenv("MODE") == "test":
                db_url = os.getenv("TEST_DB_URL")
            else:
                db_url = os.getenv("DB_URL")

            if not db_url:
                raise ValueError("Please ensure environment vairable `TEST_DB_URL` or `DB_URL` is set.")

            cls._engine = create_engine(f"postgresql+psycopg2://{db_url}")
            cls._Session = sessionmaker(cls._engine, future=True)
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def engine(self):
        return self._engine

    @property
    def Session(self):
        return self._Session


@contextmanager
def pgsql_session():
    pgsql = PostgreSQLDB()
    with pgsql.Session.begin() as session:

        Model.set_session(session)

        yield session

    Model.set_session(None)
