import requests as rq

from figure_hook.constants import SourceSite

from .abcs import ShipmentChecksum

__all__ = ["GSCShipmentChecksum"]


class GSCShipmentChecksum(ShipmentChecksum):
    __source_site__ = SourceSite.GSC_SHIPMENT

    def _extract_feature(self) -> bytes:
        url = "https://www.goodsmile.info/ja/releaseinfo"
        response = rq.get(url)
        response.raise_for_status()

        return response.content
