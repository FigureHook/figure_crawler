from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime


class Stats(UserDict, ABC):
    def __init__(self, extension_data: dict = {}) -> None:
        init_data = {
            "start_time": None,
            "finish_time": None,
        }
        init_data.update(extension_data)
        super().__init__(init_data)

    @property
    def start_time(self):
        return self.data["start_time"]

    @property
    def finish_time(self):
        return self.data["finish_time"]

    def start(self):
        if not self.start_time:
            self.data["start_time"] = datetime.utcnow()

    def finish(self):
        self.data["finish_time"] = datetime.utcnow()


class Publisher(ABC):
    @property
    @abstractmethod
    def stats(self):
        raise NotImplementedError

    @abstractmethod
    def publish(self, *args, **kwargs):
        raise NotImplementedError
