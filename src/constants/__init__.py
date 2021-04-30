from enum import Enum


class ReleaseInfoStatus(Enum):
    SAME = 1
    NEW_RELEASE = 2
    DELAY = 3
    STALLED = 4
    ALTER = 5
    CONFLICT = 6


class SourceSite(Enum):
    GSC = 1
    ALTER = 2


class PeriodicTask(Enum):
    NEWS_PUSH = 1
