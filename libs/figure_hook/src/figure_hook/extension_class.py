from dataclasses import dataclass
from datetime import date

__all__ = [
    "ReleaseFeed"
]


@dataclass
class ReleaseFeed:
    name: str
    url: str
    is_adult: bool
    series: str
    maker: str
    size: int
    scale: int
    price: int
    release_date: date
    image_url: str
    thumbnail: str
    og_image: str

    @property
    def media_image(self):
        if self.thumbnail == self.og_image:
            return self.image_url
        return self.og_image
