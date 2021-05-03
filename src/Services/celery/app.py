import os
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
        crontab(minute="*/5"),
        news_push.s(),
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

    with pgsql_session():
        webhooks: Iterable[Webhook] = Webhook.all()
        for webhook in webhooks:
            is_existed = hooker.webhook_status.get(webhook.id)
            if is_existed is not None:
                webhook.update(is_existed=is_existed)

    return hooker.stats
