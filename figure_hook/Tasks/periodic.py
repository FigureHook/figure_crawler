from abc import ABC, abstractmethod

from discord.webhook import RequestsWebhookAdapter
from sqlalchemy import select, update

from figure_hook.constants import PeriodicTask
from figure_hook.database import pgsql_session
from figure_hook.Factory.publish_factory.discord_embed_factory import \
    DiscordEmbedFactory
from figure_hook.Factory.publish_factory.plurk_content_factory import \
    PlurkContentFactory
from figure_hook.Helpers.db_helper import ReleaseHelper
from figure_hook.Models import Task, Webhook
from figure_hook.Publishers.dispatchers import \
    DiscordNewReleaseEmbedsDispatcher
from figure_hook.Publishers.plurk import Plurker


class NewReleasePush(ABC):
    __task_id__: PeriodicTask

    def __init__(self):
        with pgsql_session() as session:
            the_task = self._fetch_model(session)

            if not the_task:
                the_task = Task(
                    name=self.name
                )
                session.add(the_task)

    def _fetch_model(self, session):
        stmt = select(Task).where(Task.name == self.name)
        result = session.execute(stmt)
        the_task = result.scalar()

        return the_task

    @property
    def name(self):
        return self.task_id.name

    @property
    def task_id(self):
        return self.__task_id__

    def _fetch_new_releases(self):
        with pgsql_session() as session:
            task = self._fetch_model(session)
            releases = ReleaseHelper.fetch_new_releases(session, task.executed_at)
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

    def execute(self):
        plurker = Plurker()
        new_releases = self._fetch_new_releases()

        for release in new_releases:
            content = PlurkContentFactory.create_new_release(release)
            plurker.publish(content=content)

        return plurker.stats
