from datetime import datetime


class OrderPeriod:
    def __init__(self, start, end):
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def is_available(self, datetime):
        return self.start < datetime < self.end

    def is_available_now(self):
        return self.start < datetime.now() < self.end

    def keys(self):
        return ["start", "end"]

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return "{class_name}({start}, {end})".format(
            class_name=self.__class__.__name__,
            **self
        )


class YearlyAnnouncement:
    def __init__(self, start, end):
        if not end:
            end = datetime.now().year

        if end < start:
            raise ValueError

        self.period = range(start, end+1)
        self._current = start

    @property
    def current(self) -> int:
        return self._current

    @current.setter
    def current(self, current_year: int):
        if type(current_year) is int:
            self._current = current_year
        else:
            raise TypeError("Current should be 'int' type.")
