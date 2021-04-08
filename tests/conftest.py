import random

import pytest
from faker import Faker

from src.custom_classes import HistoricalReleases, OrderPeriod, Release
from src.Factory import ProductBase


@pytest.fixture()
def session():
    from src.database import Model, db

    with db("sqlite://", echo=False) as db:
        engine = db.engine
        session = db.session

        Model.metadata.create_all(bind=engine)

        yield session

    session.close()
    Model.metadata.drop_all(bind=engine)


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
        images=[fake.uri() for _ in range(5)]
    )

    return p
