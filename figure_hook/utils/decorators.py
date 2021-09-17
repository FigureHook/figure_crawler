from functools import wraps

from sqlalchemy_mixins.session import NoSessionError


def ensure_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
        except NoSessionError:
            raise RuntimeError(
                "Can't get session.\
                    Please ensure call Model.set_session(session) or call method in database session context."
            )
        return r
    return wrapper
