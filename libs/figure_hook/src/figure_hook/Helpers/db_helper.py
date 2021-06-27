from datetime import datetime

from figure_hook.extension_class import ReleaseFeed
from figure_hook.Models import (Company, Product, ProductOfficialImage,
                                ProductReleaseInfo, Series)
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_, literal_column


class ReleaseHelper:
    @staticmethod
    def fetch_new_releases(session: Session, time: datetime) -> list[ReleaseFeed]:
        """fetch new releases to push."""
        r = select(
            ProductReleaseInfo.product_id,
            ProductReleaseInfo.price.label('price'),
            ProductReleaseInfo.initial_release_date.label('release_date')
        ).where(
            ProductReleaseInfo.created_at > time,
            # ensure fetched data parsed by new release checking parser
            ProductReleaseInfo.announced_at.isnot(None),
            ProductReleaseInfo.announced_at >= time.date()
        ).cte("release_info")

        stmt = select(
            Product.name.label("name"),
            Product.url.label("url"),
            Product.adult.label("is_adult"),
            Product.resale.label("resale"),
            Series.name.label("series"),
            Company.name.label("maker"),
            literal_column("release_info.price").label("price"),
            literal_column("release_info.release_date").label("release_date"),
            ProductOfficialImage.url.label("image_url"),
            Product.thumbnail.label("thumbnail"),
            Product.og_image.label("og_image"),
            Product.size.label("size"),
            Product.scale.label("scale")
        ).select_from(
            Product
        ).join(
            r
        ).join(
            Product.manufacturer
        ).join(
            Product.series
        ).outerjoin(
            ProductOfficialImage,
            and_(Product.id == ProductOfficialImage.product_id,
                 ProductOfficialImage.order == 1)
        )

        releases = session.execute(stmt).all()

        release_feeds = []
        for release in releases:
            feed = ReleaseFeed(
                name=release.name,
                url=release.url,
                is_adult=release.is_adult,
                series=release.series,
                maker=release.maker,
                size=release.size,
                scale=release.scale,
                price=release.price,
                release_date=release.release_date,
                image_url=release.image_url,
                thumbnail=release.thumbnail,
                og_image=release.og_image,
                resale=release.resale,
            )
            release_feeds.append(feed)

        return release_feeds
