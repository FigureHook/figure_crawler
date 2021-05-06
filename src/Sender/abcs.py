from abc import ABC, abstractmethod


class Sender(ABC):
    @property
    @abstractmethod
    def stats(self):
        raise NotImplementedError

    @abstractmethod
    def send(self, *args, **kwargs):
        raise NotImplementedError
