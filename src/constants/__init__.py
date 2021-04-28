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


class ProcessorID(Enum):
    DISCORD_HOOKER = 1
    GSC_NEW_ANNOUN_CRAWLER = 2


class ProcessorType(Enum):
    CRAWLER = 1
    SENDER = 2


class ProcessorStatus(Enum):
    SUCCESS = 1
    WARNING = 2
    FAILED = 4
