import os
from collections import namedtuple
from typing import Iterable

from celery import Celery
from celery.schedules import crontab
from discord import RequestsWebhookAdapter

from src.constants import PeriodicTask
from src.database import pgsql_session
from src.Models import Task, Webhook
from src.Sender.discord_hooker import DiscordHooker
from src.utils.announcement_checksum import (AlterChecksum, GSCChecksum,
                                             SiteChecksum)
from src.utils.data_access import (make_discord_webhooks,
                                   make_newly_release_embeds_after)
from src.utils.scrapyd_api import schedule_spider

rabbit_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbit_pw = os.getenv("RABBITMQ_DEFAULT_PASS")

app = Celery("kappa", broker=f"pyamqp://{rabbit_user}:{rabbit_pw}@rabbit:5672//")


class Config:
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = "Asia/Taipei"
    enable_utc = True


app.config_from_object(Config)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/10"),
        news_push.s(),
        name="push new release through discord webhook",
    )
    sender.add_periodic_task(
        crontab(minute="*/30"),
        check_new_release.s(),
        name="check product every half-hour",
    )


@app.task
def news_push():
    this_task: Task
    with pgsql_session():
        this_task = Task.query.get(PeriodicTask.NEWS_PUSH)
        adapter = RequestsWebhookAdapter()
        discord_webhooks = make_discord_webhooks(adapter)
        embeds = make_newly_release_embeds_after(this_task.executed_at)
        this_task.update()
        hooker = DiscordHooker(discord_webhooks, embeds=embeds)
        hooker.send()

        webhooks: Iterable[Webhook] = Webhook.all()
        for webhook in webhooks:
            is_existed = hooker.webhook_status.get(webhook.id)
            if is_existed is not None:
                webhook.update(is_existed=is_existed)

    return hooker.stats


@app.task
def check_new_release():
    scheduled_jobs = []
    with pgsql_session():
        CheckingPair = namedtuple("CheckingPair", ["checksum_cls", "spider_name"])
        sites_to_check = [
            CheckingPair(AlterChecksum, "alter_recent"),
            CheckingPair(GSCChecksum, "gsc_recent")
        ]
        for checking_pair in sites_to_check:
            checksum: SiteChecksum = checking_pair.checksum_cls()
            if checksum.is_changed:
                response = schedule_spider(checking_pair.spider_name)
                scheduled_jobs.append(response)
                checksum.update()
    return scheduled_jobs
