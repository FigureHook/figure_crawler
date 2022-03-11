import logging
import time
from abc import ABC, abstractmethod

from discord.webhook import RequestsWebhookAdapter
from sqlalchemy import select, update

from figure_hook.constants import PeriodicTask
from figure_hook.extension_class import ReleaseFeed
from figure_hook.Factory.publish_factory.discord_embed_factory import \
    DiscordEmbedFactory
from figure_hook.Factory.publish_factory.plurk_content_factory import \
    PlurkContentFactory
from figure_hook.Helpers.db_helper import ReleaseHelper
from figure_hook.Publishers.discord_hooker import DiscordNewReleaseHooker
from figure_hook.Models import Task, Webhook
from figure_hook.exceptions import PublishError
from figure_hook.Publishers.plurk import Plurker

default_logger = logging.getLogger(__name__)


class NewReleasePush(ABC):
    __task_id__: PeriodicTask

    def __init__(self, session):
        self._session = session
        self._model = self._fetch_model() or Task.create(name=self.name)

    def _fetch_model(self):
        stmt = select(Task).where(Task.name == self.name)
        result = self.session.execute(stmt)
        the_task = result.scalar()

        return the_task

    @property
    def executed_at(self):
        return self._model.executed_at

    @property
    def session(self):
        return self._session

    @property
    def name(self):
        return self.task_id.name

    @property
    def task_id(self):
        return self.__task_id__

    def _fetch_new_releases(self):
        releases = ReleaseHelper.fetch_new_releases(
            self.session,
            self.executed_at
        )
        return releases

    def _update_execution_time(self):
        self._model.update()

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class DiscordNewReleasePush(NewReleasePush):
    __task_id__ = PeriodicTask.DISCORD_NEW_RELEASE_PUSH

    def execute(self):
        raw_embeds = [DiscordEmbedFactory.create_new_release(release) for release in self._fetch_new_releases()]
        self._update_execution_time()

        webhook_adapter = RequestsWebhookAdapter()
        publisher = DiscordNewReleaseHooker(raw_embeds=raw_embeds)

        webhooks = Webhook.all()
        for webhook in webhooks:
            publisher.publish(webhook=webhook, webhook_adapter=webhook_adapter)

        self._update_webhook_status(publisher.webhook_status)

        return publisher.stats

    def _update_webhook_status(self, webhook_status):
        for webhook_id, is_existed in webhook_status.items():
            stmt = update(Webhook).where(
                Webhook.id == webhook_id
            ).values(
                is_existed=is_existed
            ).execution_options(
                synchronize_session="fetch"
            )

            self.session.execute(stmt)


class PlurkNewReleasePush(NewReleasePush):
    failed_releases: list[ReleaseFeed]
    __task_id__ = PeriodicTask.PLURK_NEW_RELEASE_PUSH

    def __init__(self, session):
        super().__init__(session)
        self.failed_releases = []
        self.plurker = Plurker()

    def execute(self, logger: logging.Logger = default_logger):
        new_releases = self._fetch_new_releases()
        self._update_execution_time()

        for release in new_releases:
            content = PlurkContentFactory.create_new_release(release)
            try:
                self.plurker.publish(content=content)
            except PublishError as err:
                self.failed_releases.append(release)
                logger.error(err)
            finally:
                time.sleep(3)

        return self.plurker.stats
