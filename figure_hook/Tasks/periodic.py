from abc import ABC, abstractmethod

from sqlalchemy import select, update
from discord.webhook import RequestsWebhookAdapter
from figure_hook.constants import PeriodicTask
from figure_hook.database import pgsql_session
from figure_hook.Factory.publish_factory.discord_embed_factory import \
    DiscordEmbedFactory
from figure_hook.Factory.publish_factory.plurk_content_factory import \
    PlurkContentFactory
from figure_hook.Publishers.dispatchers import DiscordNewReleaseEmbedsDispatcher
from figure_hook.Helpers.db_helper import ReleaseHelper
from figure_hook.Models import Task, Webhook
import datetime


class NewReleasePush(ABC):
    __task_id__: PeriodicTask
    executed_at: datetime.datetime

    def __init__(self):
        self.executed_at = self._fetch_task_executed_time()

    @property
    def task_id(self):
        return self.__task_id__

    def _fetch_task_executed_time(self) -> Task:
        with pgsql_session() as session:
            stmt = select(Task).where(Task.name == self.task_id.name)
            result = session.execute(stmt)
            the_task = result.scalar()

            if not the_task:
                the_task = Task(
                    name=self.task_id.name
                )
                session.add(the_task)

            return the_task.executed_at

    def _fetch_new_releases(self):
        with pgsql_session() as session:
            releases = ReleaseHelper.fetch_new_releases(session, self.executed_at)
        return releases

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class DiscordNewReleasePush(NewReleasePush):
    __task_id__ = PeriodicTask.DISCORD_NEW_RELEASE_PUSH

    def execute(self):
        new_releases = self._fetch_new_releases()
        raw_embeds = []

        for release in new_releases:
            embed = DiscordEmbedFactory.create_new_release(release)
            raw_embeds.append(embed)

        with pgsql_session():
            webhooks = Webhook.all()

        webhook_adapter = RequestsWebhookAdapter()
        dispatcher = DiscordNewReleaseEmbedsDispatcher(
            webhooks=webhooks,
            raw_embeds=raw_embeds,
            adapter=webhook_adapter
        )
        dispatcher.dispatch()

        self._update_webhook_by_status(dispatcher.webhook_status)

        return dispatcher.stats


    def _update_webhook_by_status(self, webhook_status):
        with pgsql_session() as session:
            for webhook_id, is_existed in webhook_status.items():
                stmt = update(Webhook).where(
                    Webhook.id == webhook_id
                ).values(
                    is_existed=is_existed
                ).execution_options(
                    synchronize_session="fetch"
                )

                session.execute(stmt)


class PlurkNewReleasePush(NewReleasePush):
    __task_id__ = PeriodicTask.PLURK_NEW_RELEASE_PUSH
    pass
