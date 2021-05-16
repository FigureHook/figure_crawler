from datetime import datetime

from sqlalchemy import select
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_, literal_column

from Models import (Company, Product, ProductOfficialImage, ProductReleaseInfo,
                    Series)


class ReleaseHelper:
    @staticmethod
    def fetch_new_releases(session: Session, time: datetime) -> list[Row]:
        """fetch new releases to push.

        return list of Row with

        `_fields('name', 'url', 'is_adult', 'series', 'maker', 'price', 'release_date', 'image_url', 'thumbnail', 'og_image')`
        """
        r = select(
            ProductReleaseInfo.product_id,
            ProductReleaseInfo.price.label('price'),
            ProductReleaseInfo.initial_release_date.label('release_date')
        ).where(
            ProductReleaseInfo.created_at > time,
            # ensure fetched data parsed by new release checking parser
            ProductReleaseInfo.announced_at.isnot(None)
        ).cte("release_info")

        stmt = select(
            Product.name.label("name"),
            Product.url.label("url"),
            Product.adult.label("is_adult"),
            Series.name.label("series"),
            Company.name.label("maker"),
            literal_column("release_info.price").label("price"),
            literal_column("release_info.release_date").label("release_date"),
            ProductOfficialImage.url.label("image_url"),
            Product.thumbnail.label("thumbnail"),
            Product.og_image.label("og_image"),
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
            and_(Product.id == ProductOfficialImage.product_id, ProductOfficialImage.order == 1)
        )

        releases = session.execute(stmt).all()
        return releases
