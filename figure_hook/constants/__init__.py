from enum import Enum


class SourceSite:
    GSC_ANNOUNCEMENT = "gsc_announcement"
    GSC_SHIPMENT = "gsc_shipment"
    GSC_DELAY = "gsc_delay"
    ALTER_ANNOUNCEMENT = "alter_announcement"
    NATIVE_ANNOUNCEMENT = "native_announcement"


class PeriodicTask(Enum):
    DISCORD_NEW_RELEASE_PUSH = 1
    PLURK_NEW_RELEASE_PUSH = 2
