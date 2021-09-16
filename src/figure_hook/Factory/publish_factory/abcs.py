from abc import ABC, abstractmethod
from typing import Any

from figure_hook.extension_class import ReleaseFeed


class PublishFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_new_release(release_feed: ReleaseFeed) -> Any:
        pass
