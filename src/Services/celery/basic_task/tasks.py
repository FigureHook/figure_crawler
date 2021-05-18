from collections import namedtuple
from typing import Type

from discord import RequestsWebhookAdapter, Webhook
from sqlalchemy.sql import update

from constants import PeriodicTask
from database import pgsql_session
from Dispatchers.discord_hook_dispatcher import \
    DiscordNewReleaseEmbedsDispatcher
from Factory.discord_embed_factory import DiscordEmbedFactory, NewReleaseEmbed
from Helpers.db_helper import ReleaseHelper
from Models import Task
from Models import Webhook as WebhookModel
from Sender.discord_hooker import DiscordHooker
from utils.announcement_checksum import (AlterChecksum, GSCChecksum,
                                         SiteChecksum)
from utils.scrapyd_api import schedule_spider

from .celery import app


@app.task
def news_push():
    this_task: Task
    with pgsql_session() as session:
        this_task = Task.query.get(PeriodicTask.NEWS_PUSH)
        new_releases = ReleaseHelper.fetch_new_releases(session, this_task.executed_at)  # type: ignore
        raw_embeds: list[NewReleaseEmbed] = []
        for r in new_releases:
            is_lazy_og_image = r.thumbnail == r.og_image
            image = r.image_url if is_lazy_og_image else r.og_image
            embed = DiscordEmbedFactory.create_new_release(
                name=r.name,
                url=r.url,
                series=r.series,
                maker=r.maker,
                price=r.price,
                image=image,
                release_date=r.release_date,
                is_adult=r.is_adult,
                thumbnail=r.thumbnail
            )
            raw_embeds.append(embed)
        this_task.update()

        webhooks: list[WebhookModel] = WebhookModel.all()
        webhook_adapter = RequestsWebhookAdapter()
        dispatcher = DiscordNewReleaseEmbedsDispatcher(webhooks, raw_embeds, webhook_adapter)
        dispatcher.dispatch()

        for webhook_id, is_existed in dispatcher.webhook_status.items():
            update(WebhookModel).where(WebhookModel.id == webhook_id).values(is_existed=is_existed)

    return dispatcher.stats


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
            checksum_cls: Type[SiteChecksum] = checking_pair.checksum_cls
            spider = checking_pair.spider_name
            checksum = checksum_cls()
            if checksum.is_changed:
                response = schedule_spider(spider)
                scheduled_jobs.append(response)
                checksum.update()
    return scheduled_jobs


@app.task
def send_new_hook_notification(webhook_id, webhook_token, msg):
    adapter = RequestsWebhookAdapter()
    embed = DiscordEmbedFactory.create_new_hook_notification(msg)
    webhook = Webhook.partial(webhook_id, webhook_token, adapter=adapter)
    hooker = DiscordHooker()
    hooker.send(webhook, [embed])
    return hooker.stats
