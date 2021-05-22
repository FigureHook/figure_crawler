import os
from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from Models.base import Model

# https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session


class PostgreSQLDB:
    _engine: Optional[Engine]
    _Session: sessionmaker

    def __init__(self):
        db_url = os.getenv("POSTGRES_URL")
        db_user = os.getenv('POSTGRES_USER')
        db_pw = os.getenv('POSTGRES_PASSWORD')
        database = os.getenv('POSTGRES_DATABASE')
        self._engine = create_engine(
            f"postgresql+psycopg2://{db_user}:{db_pw}@{db_url}/{database}",
            echo=False,
            future=True
        )
        self._Session = sessionmaker(self._engine)

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
