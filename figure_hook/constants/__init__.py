from enum import Enum


class ReleaseInfoStatus(Enum):
    SAME = 1
    NEW_RELEASE = 2
    DELAY = 3
    STALLED = 4
    ALTER = 5
    CONFLICT = 6


class SourceSite:
    GSC_ANNOUNCEMENT = "gsc_announcement"
    ALTER_ANNOUNCEMENT = "alter_announcement"
    NATIVE_ANNOUNCEMENT = "native_announcement"


class PeriodicTask(Enum):
    DISCORD_NEW_RELEASE_PUSH = 1
    PLURK_NEW_RELEASE_PUSH = 2
