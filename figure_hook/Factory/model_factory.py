from typing import List

from figure_hook.constants import ReleaseInfoStatus
from figure_hook.Models import Category, Company, Paintwork
from figure_hook.Models import Product as Product
from figure_hook.Models import (ProductOfficialImage, ProductReleaseInfo,
                                Sculptor, Series)
from figure_hook.utils.comparater import compare_release_infos
from figure_parser.extension_class import HistoricalReleases, Release
from figure_parser.product import ProductBase

__all__ = (
    "ProductModelFactory",
)


class ProductModelFactory:
    @staticmethod
    def createProduct(product_dataclass: ProductBase) -> Product:
        series = Series.as_unique(name=product_dataclass.series)
        manufacturer = Company.as_unique(name=product_dataclass.manufacturer)
        category = Category.as_unique(name=product_dataclass.category)
        releaser = Company.as_unique(name=product_dataclass.releaser)
        distributer = Company.as_unique(name=product_dataclass.distributer)

        paintworks = Paintwork.multiple_as_unique(product_dataclass.paintworks)
        sculptors = Sculptor.multiple_as_unique(product_dataclass.sculptors)

        images = ProductOfficialImage.create_image_list(
            product_dataclass.images
        )

        release_infos: List[ProductReleaseInfo] = []
        for release in product_dataclass.release_infos:
            release_info = ProductReleaseInfo(
                price=release.price,
                initial_release_date=release.release_date,
                announced_at=release.announced_at
            )
            if release.price:
                release_info.tax_including = release.price.tax_including
            release_infos.append(release_info)

        product = Product.create(
            url=product_dataclass.url,
            name=product_dataclass.name,
            size=product_dataclass.size,
            scale=product_dataclass.scale,
            resale=product_dataclass.resale,
            adult=product_dataclass.adult,
            copyright=product_dataclass.copyright,
            series=series,
            manufacturer=manufacturer,
            releaser=releaser,
            distributer=distributer,
            category=category,
            id_by_official=product_dataclass.maker_id,
            checksum=product_dataclass.checksum,
            jan=product_dataclass.jan,
            order_period_start=product_dataclass.order_period.start,
            order_period_end=product_dataclass.order_period.end,
            thumbnail=product_dataclass.thumbnail,
            og_image=product_dataclass.og_image,
            # relationship
            release_infos=release_infos,
            sculptors=sculptors,
            paintworks=paintworks,
            official_images=images
        )

        return product

    @staticmethod
    def updateProduct(product_dataclass: ProductBase, product_model: Product):
        status = compare_release_infos(product_dataclass, product_model)

        last_release_form_dataclass = product_dataclass.release_infos.last()
        last_release_form_model = product_model.last_release()

        if status is ReleaseInfoStatus.SAME:
            pass
        elif status is ReleaseInfoStatus.NEW_RELEASE:
            new_release = ProductReleaseInfo(
                initial_release_date=last_release_form_dataclass.release_date,
                price=last_release_form_dataclass.price,
                announced_at=last_release_form_dataclass.announced_at
            )
            if last_release_form_dataclass.price:
                new_release.tax_including = last_release_form_dataclass.price.tax_including
            product_model.release_infos.append(new_release)
        elif status is ReleaseInfoStatus.DELAY:
            new_release_date = last_release_form_dataclass.release_date
            last_release_form_model.postpone_release_date_to(new_release_date)
        elif status is ReleaseInfoStatus.STALLED:
            last_release_form_model.stall()
        elif status is ReleaseInfoStatus.ALTER:
            rebuild_release_infos(
                product_dataclass.release_infos,
                product_model.release_infos
            )
        elif status is ReleaseInfoStatus.CONFLICT:
            raise ReleaseInfosConflictError(product_dataclass.url)

        series = Series.as_unique(name=product_dataclass.series)
        manufacturer = Company.as_unique(name=product_dataclass.manufacturer)
        category = Category.as_unique(name=product_dataclass.category)
        releaser = Company.as_unique(name=product_dataclass.releaser)
        distributer = Company.as_unique(name=product_dataclass.distributer)

        paintworks = Paintwork.multiple_as_unique(product_dataclass.paintworks)
        sculptors = Sculptor.multiple_as_unique(product_dataclass.sculptors)

        product_model.update(
            url=product_dataclass.url,
            name=product_dataclass.name,
            size=product_dataclass.size,
            scale=product_dataclass.scale,
            resale=product_dataclass.resale,
            adult=product_dataclass.adult,
            copyright=product_dataclass.copyright,
            series=series,
            manufacturer=manufacturer,
            releaser=releaser,
            distributer=distributer,
            category=category,
            id_by_official=product_dataclass.maker_id,
            checksum=product_dataclass.checksum,
            order_period_start=product_dataclass.order_period.start,
            order_period_end=product_dataclass.order_period.end,
            thumbnail=product_dataclass.thumbnail,
            og_image=product_dataclass.og_image,
            # relationship
            sculptors=sculptors,
            paintworks=paintworks,
        )

        return product_model


def rebuild_release_infos(
    parsed_infos: HistoricalReleases[Release],
    model_infos: List[ProductReleaseInfo]
) -> List[ProductReleaseInfo]:
    for dr, mr in zip(parsed_infos, model_infos):
        mr.update(price=dr.price)
        if dr.price:
            mr.update(tax_including=dr.price.tax_including)
        if dr.release_date:
            if dr.release_date < mr.initial_release_date:
                mr.update(initial_release_date=dr.release_date)
            else:
                mr.postpone_release_date_to(dr.release_date)
    return model_infos


class ReleaseInfosConflictError(Exception):
    def __init__(self, url):
        message = f"parsed release_infos were less than release_infos in Modal.({url})"
        super().__init__(message)
