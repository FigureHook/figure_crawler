import os
import random

import pytest
from faker import Faker
from figure_parser.extension_class import (HistoricalReleases, OrderPeriod,
                                           Release)
from figure_parser.product import ProductBase

os.environ['POSTGRES_DATABASE'] = "figure_testing"


@pytest.fixture()
def session():
    from sqlalchemy.orm import Session

    from figure_hook.database import PostgreSQLDB
    from figure_hook.Models.base import Model

    pgsql = PostgreSQLDB()

    with Session(pgsql.engine) as session:
        Model.set_session(session)
        Model.metadata.create_all(bind=pgsql.engine)
        yield session

    Model.set_session(None)  # type: ignore
    Model.metadata.drop_all(bind=pgsql.engine)


@pytest.fixture()
def release_feed():
    from figure_hook.extension_class import ReleaseFeed
    fake = Faker(['ja-JP'])
    return ReleaseFeed(
        name=fake.name(),
        url=fake.url(),
        is_adult=fake.boolean(chance_of_getting_true=25),
        resale=fake.boolean(chance_of_getting_true=25),
        series=fake.name(),
        maker=fake.name(),
        scale=random.randint(1, 30),
        size=random.randint(1, 1000),
        price=random.randint(1000, 1000000),
        release_date=fake.date_object(),
        image_url=fake.uri(),
        thumbnail=fake.uri(),
        og_image=fake.uri()
    )


@pytest.fixture()
def product():
    from figure_parser.extension_class import Price
    fake = Faker(['ja-JP'])

    release_infos = HistoricalReleases()
    for _ in range(random.randint(1, 4)):
        release_infos.append(
            Release(
                release_date=fake.date_object(),
                price=Price(random.randint(1000, 1000000),
                            fake.boolean(chance_of_getting_true=25))
            )
        )

    p = ProductBase(
        url=fake.url(),
        name=fake.name(),
        series=fake.name(),
        manufacturer=fake.company(),
        category=fake.name(),
        price=Price(random.randint(1000, 1000000),
                    fake.boolean(chance_of_getting_true=25)),
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
