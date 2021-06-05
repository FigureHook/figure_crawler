import os
from contextlib import contextmanager

from figure_hook.Models.base import Model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session


class PostgreSQLDB:
    __instance__ = None

    def __new__(cls) -> 'PostgreSQLDB':
        if not cls.__instance__:
            db_url = os.getenv("POSTGRES_URL")
            db_user = os.getenv('POSTGRES_USER')
            db_pw = os.getenv('POSTGRES_PASSWORD')
            database = os.getenv('POSTGRES_DATABASE')
            cls._engine = create_engine(
                f"postgresql+psycopg2://{db_user}:{db_pw}@{db_url}/{database}",
                echo=False,
                future=True
            )
            cls._sessionmaker = sessionmaker(cls._engine)
            cls.__instance__ = super().__new__(cls)

        return cls.__instance__

    @property
    def engine(self):
        return self._engine

    @property
    def Session(self):
        return self._sessionmaker


@contextmanager
def pgsql_session():
    pgsql = PostgreSQLDB()
    with pgsql.Session.begin() as session:

        Model.set_session(session)

        yield session

    Model.set_session(None)  # type: ignore
