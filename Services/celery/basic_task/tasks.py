from typing import Type

from discord import RequestsWebhookAdapter, Webhook
from figure_hook.constants import PeriodicTask
from figure_hook.database import pgsql_session
from figure_hook.Factory.publish_factory.discord_embed_factory import (
    DiscordEmbedFactory, NewReleaseEmbed)
from figure_hook.Factory.publish_factory.plurk_content_factory import \
    PlurkContentFactory
from figure_hook.Helpers.db_helper import ReleaseHelper
from figure_hook.Models import Task
from figure_hook.Models import Webhook as WebhookModel
from figure_hook.Publishers import DiscordHooker, Plurker
from figure_hook.Publishers.dispatchers import \
    DiscordNewReleaseEmbedsDispatcher
from figure_hook.utils.announcement_checksum import (AlterChecksum,
                                                     GSCChecksum,
                                                     NativeChecksum,
                                                     SiteChecksum)
from sqlalchemy.sql import update

from .celery import app


@app.task
def news_push():
    """FIXME: so ugly
    """
    this_task: Task
    with pgsql_session() as session:
        this_task = session.query(Task).where(
            Task.name == PeriodicTask.NEWS_PUSH
        ).scalar()
        new_releases = ReleaseHelper.fetch_new_releases(
            session, this_task.executed_at  # type: ignore
        )
        raw_embeds: list[NewReleaseEmbed] = []
        plurker = Plurker()
        for r in new_releases:
            # Discord embed
            embed = DiscordEmbedFactory.create_new_release(r)
            raw_embeds.append(embed)

            # Plurk
            plurk = PlurkContentFactory.create_new_release(r)
            plurker.publish(content=plurk)

        this_task.update()

        webhooks: list[WebhookModel] = WebhookModel.all()  # type: ignore

        # begin dispatching embeds
        dispatcher = DiscordNewReleaseEmbedsDispatcher(
            webhooks,
            raw_embeds
        )
        dispatcher.dispatch()  # long-time job

    with pgsql_session() as session:
        for webhook_id, is_existed in dispatcher.webhook_status.items():
            stmt = update(WebhookModel).where(
                WebhookModel.id == webhook_id
            ).values(
                is_existed=is_existed
            ).execution_options(
                synchronize_session="fetch"
            )

            session.execute(stmt)

    return {
        "discord": dispatcher.stats,
        "plurk": plurker.stats,
    }


@app.task
def check_new_release():
    scheduled_jobs = []
    site_checksums: list[Type[SiteChecksum]] = [
        AlterChecksum,
        GSCChecksum,
        NativeChecksum
    ]
    with pgsql_session():
        for site_checksum in site_checksums:
            checksum = site_checksum()
            if checksum.is_changed:
                spider_jobs = checksum.trigger_crawler()
                scheduled_jobs.extend(spider_jobs)
                checksum.update()
    return scheduled_jobs


@app.task
def send_new_hook_notification(webhook_id, webhook_token, msg):
    adapter = RequestsWebhookAdapter()
    embed = DiscordEmbedFactory.create_new_hook_notification(msg)
    webhook = Webhook.partial(webhook_id, webhook_token, adapter=adapter)
    hooker = DiscordHooker()
    hooker.publish(webhook, [embed])
    return hooker.stats
