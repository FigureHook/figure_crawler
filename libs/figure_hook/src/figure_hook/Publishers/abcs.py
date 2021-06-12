from abc import ABC, abstractmethod


class Publisher(ABC):
    @property
    @abstractmethod
    def stats(self):
        raise NotImplementedError

    @abstractmethod
    def publish(self, *args, **kwargs):
        raise NotImplementedError
