import os
from contextlib import contextmanager
from dataclasses import dataclass
from typing import ClassVar, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .Models.base import Model

# https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session


@dataclass(frozen=True)
class DbSession:
    engine: Engine
    session: scoped_session


class PostgreSQLDB:
    _instance = None

    _engine: ClassVar[Optional[Engine]] = None
    _db_url = os.environ.get("DB_URL")
    _Session = None

    def __new__(cls):
        if not cls._instance:
            cls._engine = create_engine(cls._db_url)
            cls._Session = sessionmaker(cls._engine)
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


@contextmanager
def db(db_url=None, echo=True):
    """ Creates a context with an open SQLAlchemy session.
    """
    if not db_url:
        db_url = os.environ.get("DB_URL", "sqlite:///db/app.sqlite")

    engine = create_engine(db_url, echo=echo)
    Session = sessionmaker(bind=engine)
    session = scoped_session(Session)

    db_session = DbSession(engine, session)

    connection = engine.connect()
    Model.set_session(session)

    yield db_session

    Model.set_session(None)
    session.close()
    connection.close()
