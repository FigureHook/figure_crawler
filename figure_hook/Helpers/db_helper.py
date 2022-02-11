from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_

from figure_hook.extension_class import ReleaseFeed
from figure_hook.Models import (Company, Product, ProductOfficialImage,
                                ProductReleaseInfo, Series)


def _make_release_feed_statement(where_clause):
    """Release feed query statement maker."""
    stmt = select(
        ProductReleaseInfo.id.label("release_id"),
        Product.name.label("name"),
        Product.url.label("url"),
        Product.adult.label("is_adult"),
        Product.resale.label("resale"),
        Series.name.label("series"),
        Company.name.label("maker"),
        ProductReleaseInfo.price.label("price"),
        ProductReleaseInfo.initial_release_date.label("release_date"),
        ProductOfficialImage.url.label("image_url"),
        Product.thumbnail.label("thumbnail"),
        Product.og_image.label("og_image"),
        Product.size.label("size"),
        Product.scale.label("scale")
    ).select_from(
        Product
    ).where(
        where_clause
    ).join(
        ProductReleaseInfo, ProductReleaseInfo.product_id == Product.id,
    ).join(
        Company, Company.id == Product.manufacturer_id
    ).join(
        Series, Series.id == Product.series_id, isouter=True
    ).join(
        ProductOfficialImage,
        and_(Product.id == ProductOfficialImage.product_id,
             ProductOfficialImage.order == 1),
    )

    return stmt


def _fetch_releases_from_created_time(session: Session, time_checkpoint: datetime):
    stmt = _make_release_feed_statement(ProductReleaseInfo.created_at >= time_checkpoint)
    releases = session.execute(stmt).all()
    return releases


def _fetch_release_by_id(session: Session, release_ids: list[int]):
    stmt = _make_release_feed_statement(ProductReleaseInfo.id.in_(release_ids))
    releases = session.execute(stmt).all()
    return releases


def _make_release_feed(release):
    feed = ReleaseFeed(
        id=release.release_id,
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
    return feed


class ReleaseHelper:
    @staticmethod
    def fetch_new_releases(session: Session, time: datetime) -> list[ReleaseFeed]:
        """fetch new releases to push."""
        releases = _fetch_releases_from_created_time(session, time)

        release_feeds: list[ReleaseFeed] = []
        for release in releases:
            feed = _make_release_feed(release)
            release_feeds.append(feed)

        return release_feeds

    @staticmethod
    def fetch_release_feed_by_ids(session: Session, release_ids: list[int]) -> list[ReleaseFeed]:
        """fetch release feed by release id"""
        releases = _fetch_release_by_id(session, release_ids)

        release_feeds: list[ReleaseFeed] = []
        for release in releases:
            feed = _make_release_feed(release)
            release_feeds.append(feed)

        return release_feeds
