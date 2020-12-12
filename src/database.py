import os
from contextlib import contextmanager

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_mixins import AllFeaturesMixin
from sqlalchemy_mixins.timestamp import TimestampsMixin

# https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session


class DbSession:
    def __init__(self, engine, session) -> None:
        super().__init__()
        self.__engine = engine
        self.__session = session

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session


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


def _unique(session, cls, hashfunc, queryfunc, constructor, arg, kw):
    """
    https://github.com/sqlalchemy/sqlalchemy/wiki/UniqueObject
    """
    cache = getattr(session, "_unique_cache", None)
    if cache is None:
        session._unique_cache = cache = {}

    key = (cls, hashfunc(*arg, **kw))
    if key in cache:
        return cache[key]
    else:
        with session.no_autoflush:
            q = session.query(cls)
            q = queryfunc(q, *arg, **kw)
            obj = q.first()
            if not obj:
                obj = constructor(*arg, **kw)
                session.add(obj)
        cache[key] = obj
        return obj


class UniqueMixin(object):
    @classmethod
    def unique_hash(cls, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def unique_filter(cls, query, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def as_unique(cls, session, *arg, **kw):
        return _unique(
            session,
            cls,
            cls.unique_hash,
            cls.unique_filter,
            cls,
            arg, kw
        )


class Model(AllFeaturesMixin):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class PkModel(Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None


class PkModelWithTimestamps(PkModel, TimestampsMixin):
    __abstract__ = True
