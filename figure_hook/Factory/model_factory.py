from typing import List

from figure_parser.product import ProductBase

from figure_hook.exceptions import ReleaseInfosConflictError
from figure_hook.Models import Category, Company, Paintwork
from figure_hook.Models import Product as ProductModel
from figure_hook.Models import (ProductOfficialImage, ProductReleaseInfo,
                                Sculptor, Series)
from figure_hook.Helpers.release_info_helper import (ReleaseInfoHelper,
                                                     ReleaseInfosSolution,
                                                     ReleaseInfosStatus)

__all__ = (
    "ProductModelFactory",
)


class ProductModelFactory:
    @staticmethod
    def create_product(product_dataclass: ProductBase) -> ProductModel:
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

        product = ProductModel.create(
            url=product_dataclass.url,
            name=product_dataclass.name,
            size=product_dataclass.size,
            scale=product_dataclass.scale,
            rerelease=product_dataclass.rerelease,
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
    def update_product(product_dataclass: ProductBase, product_model: ProductModel) -> ProductModel:
        """Should be called in database session.
        :raise ReleaseInfosConflictError: Unable to sync the release_infos
        """
        release_info_solution = ReleaseInfosSolution()

        status = ReleaseInfoHelper.compare_infos(product_dataclass.release_infos, product_model.release_infos)
        while status is not ReleaseInfosStatus.SAME and status is not ReleaseInfosStatus.CONFLICT:
            release_info_solution.set_situation(status).execute(
                product_dataclass=product_dataclass, product_model=product_model)
            status = ReleaseInfoHelper.compare_infos(product_dataclass.release_infos, product_model.release_infos)

        if status is ReleaseInfosStatus.CONFLICT:
            raise ReleaseInfosConflictError(product_dataclass.url)

        # unique attribute
        series = Series.as_unique(name=product_dataclass.series)
        manufacturer = Company.as_unique(name=product_dataclass.manufacturer)
        category = Category.as_unique(name=product_dataclass.category)
        releaser = Company.as_unique(name=product_dataclass.releaser)
        distributer = Company.as_unique(name=product_dataclass.distributer)

        # unique in list attribute
        paintworks = Paintwork.multiple_as_unique(product_dataclass.paintworks)
        sculptors = Sculptor.multiple_as_unique(product_dataclass.sculptors)

        product_model.update(
            url=product_dataclass.url,
            name=product_dataclass.name,
            size=product_dataclass.size,
            scale=product_dataclass.scale,
            rerelease=product_model.rerelease or product_dataclass.rerelease,
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
            jan=product_dataclass.jan,
            # relationship
            sculptors=sculptors,
            paintworks=paintworks,
        )

        return product_model
