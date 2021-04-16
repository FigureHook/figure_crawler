import os
from contextlib import contextmanager
from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .Models.base import Model

# https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session


@dataclass(frozen=True)
class DbSession:
    engine: Engine
    session: scoped_session


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
