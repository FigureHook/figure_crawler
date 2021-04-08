from src.Adapters import ReleaseToProductReleaseInfoModelAdapter
from src.custom_classes import Release
from src.Models import Category, Company, Paintwork
from src.Models import Product as ProductModel
from src.Models import (ProductOfficialImage, ProductReleaseInfo, Sculptor,
                        Series)

from .product import ProductBase

__all__ = ["ProductModelFactory"]


# def


class ProductModelFactory:
    @staticmethod
    def createProduct(product_dataclass: ProductBase) -> ProductModel:
        series = Series.as_unique(name=product_dataclass.series)
        manufacturer = Company.as_unique(name=product_dataclass.manufacturer)
        category = Category.as_unique(name=product_dataclass.category)
        releaser = Company.as_unique(name=product_dataclass.releaser)
        distributer = Company.as_unique(name=product_dataclass.distributer)

        paintworks = Paintwork.multiple_as_unique(product_dataclass.paintworks)
        sculptors = Sculptor.multiple_as_unique(product_dataclass.sculptors)

        images = ProductOfficialImage.create_image_list(product_dataclass.images)

        release_infos = []
        for release in product_dataclass.release_infos:
            release: Release
            release_info = ReleaseToProductReleaseInfoModelAdapter(release)
            release_infos.append(release_info)

        product = ProductModel.create(
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
            # relationship
            release_infos=release_infos,
            sculptors=sculptors,
            paintworks=paintworks,
            official_images=images
        )

        return product

    # FIXME: how to update Product?
    @staticmethod
    def updateProduct(session, product_dataclass: ProductBase, product_model: ProductModel):
        is_delay: bool = check_delay()
        is_new_release: bool = check_new_release()
        release_should_be_updated: bool = is_delay or is_new_release

        if release_should_be_updated:
            if is_delay:
                last_release: ProductReleaseInfo = get_last_release()
                last_release.postpone_release_date_to(product_dataclass.release_date)
            if is_new_release:
                new_release = ReleaseToProductReleaseInfoModelAdapter(product_dataclass.release_infos.last())
                product_model.release_infos.append(new_release)
                product_model.resale = True

        series = Series.as_unique(session, name=product_dataclass.series)
        manufacturer = Company.as_unique(session, name=product_dataclass.manufacturer)
        category = Category.as_unique(session, name=product_dataclass.category)
        releaser = Company.as_unique(session, name=product_dataclass.releaser)
        distributer = Company.as_unique(session, name=product_dataclass.distributer)

        paintworks = Paintwork.multiple_as_unique(session, product_dataclass.paintworks)
        sculptors = Sculptor.multiple_as_unique(session, product_dataclass.sculptors)

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
            # relationship
            sculptors=sculptors,
            paintworks=paintworks,
        )

        raise NotImplementedError
