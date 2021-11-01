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
    NATIVE = 3


class PeriodicTask(Enum):
    DISCORD_NEW_RELEASE_PUSH = 1
    PLURK_NEW_RELEASE_PUSH = 2
