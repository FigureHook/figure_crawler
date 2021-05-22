import os
import random
from unittest.mock import MagicMock

import pytest
from faker import Faker

from Parsers.extension_class import HistoricalReleases, OrderPeriod, Release
from Parsers.product import ProductBase

os.environ['POSTGRES_DATABASE'] = "figure_testing"
os.environ['FLASK_ENV'] = "test"


@pytest.fixture(scope='session')
def app():
    from Services.web import utils
    utils.get_maintenance_time = MagicMock(return_value="Wed, 21 Oct 2015 07:28:00 GMT")
    from database import PostgreSQLDB
    from Models.base import Model
    from Services.web.app import create_app

    app = create_app("test")
    pgsql = PostgreSQLDB()
    Model.metadata.create_all(pgsql.engine)

    yield app

    Model.metadata.drop_all(pgsql.engine)


@pytest.fixture()
def session():
    from sqlalchemy.orm import Session

    from database import PostgreSQLDB
    from Models.base import Model

    pgsql = PostgreSQLDB()

    with Session(pgsql.engine) as session:
        Model.set_session(session)
        Model.metadata.create_all(bind=pgsql.engine)
        yield session

    Model.set_session(None)
    Model.metadata.drop_all(bind=pgsql.engine)


@pytest.fixture()
def product():
    fake = Faker(['ja-JP'])

    release_infos = HistoricalReleases()
    for _ in range(random.randint(1, 4)):
        release_infos.append(
            Release(
                release_date=fake.date_object(),
                price=random.randint(1000, 1000000)
            )
        )

    p = ProductBase(
        url=fake.url(),
        name=fake.name(),
        series=fake.name(),
        manufacturer=fake.company(),
        category=fake.name(),
        price=random.randint(1000, 1000000),
        release_date=fake.date_object(),
        release_infos=release_infos,
        order_period=OrderPeriod(fake.date_time()),
        size=random.randint(1, 1000),
        scale=random.randint(1, 30),
        sculptors=[fake.name() for _ in range(2)],
        paintworks=[fake.name() for _ in range(2)],
        resale=fake.boolean(chance_of_getting_true=25),
        adult=fake.boolean(chance_of_getting_true=30),
        copyright=fake.text(max_nb_chars=20),
        releaser=fake.company(),
        distributer=fake.company(),
        jan=fake.jan13(),
        maker_id=str(random.randint(1, 1000)),
        images=[fake.uri() for _ in range(5)],
        thumbnail=fake.uri(),
        og_image=fake.uri(),
    )

    return p
