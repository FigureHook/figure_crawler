import os
from unittest.mock import MagicMock

import pytest

os.environ['POSTGRES_DATABASE'] = "figure_testing"
os.environ['FLASK_ENV'] = "test"


@pytest.fixture(scope='session')
def app():
    from Services.web import callbacks
    callbacks.get_maintenance_time = MagicMock(return_value="Wed, 21 Oct 2015 07:28:00 GMT")
    from figure_hook.database import PostgreSQLDB
    from figure_hook.Models.base import Model

    from Services.web.app import create_app

    app = create_app("test")
    pgsql = PostgreSQLDB()
    Model.metadata.create_all(pgsql.engine)

    yield app

    Model.metadata.drop_all(pgsql.engine)


@pytest.fixture()
def session():
    from figure_hook.database import PostgreSQLDB
    from figure_hook.Models.base import Model
    from sqlalchemy.orm import Session

    pgsql = PostgreSQLDB()

    with Session(pgsql.engine) as session:
        Model.set_session(session)
        Model.metadata.create_all(bind=pgsql.engine)
        yield session

    Model.set_session(None)
    Model.metadata.drop_all(bind=pgsql.engine)
