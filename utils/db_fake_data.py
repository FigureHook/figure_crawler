import random
from datetime import datetime

from faker import Faker
from figure_parser.product import (HistoricalReleases, OrderPeriod, Price,
                                   Product, Release)

from figure_hook.Factory import ProductModelFactory
from figure_hook.Models import ProductReleaseInfo, Webhook, Task
from figure_hook.constants import PeriodicTask

fake = Faker(['ja-JP'])


def create_fake_task() -> list[Task]:
    executed_time = datetime(2017, 5, 5)
    ds_task = Task(
        name=PeriodicTask.DISCORD_NEW_RELEASE_PUSH.name,
        executed_at=executed_time
    )
    plurk_task = Task(
        name=PeriodicTask.PLURK_NEW_RELEASE_PUSH.name,
        executed_at=executed_time
    )

    return [ds_task, plurk_task]


def create_fake_webhooks(amount: int) -> list[Webhook]:
    webhooks = []
    for _ in range(amount):
        webhook = Webhook(
            id=fake.lexify(text='?????????????'),
            channel_id=fake.lexify(text='?????????????'),
            token=fake.lexify(text='?????????????'),
            is_nsfw=fake.boolean(chance_of_getting_true=80),
            lang=fake.random_element(elements=Webhook.supporting_langs)
        )
        webhooks.append(webhook)

    return webhooks


def create_fake_products(amount: int) -> list[Product]:
    products = []

    release_infos = HistoricalReleases()
    for _ in range(random.randint(1, 4)):
        release_infos.append(
            Release(
                announced_at=fake.date_time_between(
                    start_date=datetime(2015, 1, 1),
                    end_date=datetime(2018, 12, 31)
                ),
                release_date=fake.date_time_between(
                    start_date=datetime(2019, 1, 1),
                    end_date=datetime(2021, 12, 31)
                ),
                price=Price(
                    random.randint(1000, 1000000),
                    fake.boolean(chance_of_getting_true=25)
                ),
            )
        )
    for _ in range(amount):
        product = Product(
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

        products.append(product)
    return products


def update_fake_release_created_time(session):
    prs = ProductReleaseInfo.all()
    for pr in prs:
        pr.created_at = fake.date_time_between(
            start_date=datetime(2015, 1, 1),
            end_date=datetime(2020, 12, 31)
        )
        session.add(pr)


def insert_fake_products(session):
    products = create_fake_products(100)
    for p in products:
        product_model = ProductModelFactory.createProduct(p)
        session.add(product_model)


def insert_fake_webhooks(session):
    for _ in range(10):
        random_lang, *_ = fake.random_choices(
            elements=Webhook.supporting_langs
        )
        webhook = Webhook(
            id=fake.numerify(text='%###########'),
            channel_id=fake.lexify(text='?????????????'),
            token=fake.lexify(text='?????????????'),
            lang=random_lang
        )
        session.add(webhook)


def insert_fake_tasks(session):
    for task in create_fake_task():
        session.add(task)
