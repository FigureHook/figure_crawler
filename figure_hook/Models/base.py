from typing import Any, AnyStr, Optional, Type, TypeVar, Union

from sqlalchemy import Column, Integer
from sqlalchemy_mixins import AllFeaturesMixin
from sqlalchemy_mixins.timestamp import TimestampsMixin


class Model(AllFeaturesMixin):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


P = TypeVar('P', bound='PkModel')


class PkModel(Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get_by_id(cls: Type[P], record_id: Union[AnyStr, int]) -> Optional[P]:
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.session.get(cls, int(record_id))
        return None


class PkModelWithTimestamps(PkModel, TimestampsMixin):
    __abstract__ = True


class UniqueMixin(Model):
    """
    https://github.com/sqlalchemy/sqlalchemy/wiki/UniqueObject
    """
    __abstract__ = True

    @classmethod
    def unique_hash(cls, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def unique_filter(cls, query, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def as_unique(cls, *arg: Any, **kw: Any):
        return _unique(
            cls.session,
            cls,
            cls.unique_hash,
            cls.unique_filter,
            cls,
            arg, kw
        )


T = TypeVar('T')


def _unique(session, cls: Type[T], hashfunc, queryfunc, constructor, arg, kw) -> Optional[T]:
    cache = getattr(session, '_unique_cache', None)
    if cache is None:
        session._unique_cache = cache = {}

    hash_value = hashfunc(*arg, **kw)
    if not hash_value:
        return None

    key = (cls, hash_value)
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
