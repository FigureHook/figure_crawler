from src.Adapters import ReleaseToProductReleaseInfoModelAdapter
from src.custom_classes import Release
from src.Models import (Category, Company, Paintwork, Product,
                        ProductOfficialImage, ProductReleaseInfo, Sculptor,
                        Series)

from .product import ProductBase

__all__ = ["ProductModelFactory"]


class ProductModelFactory:
    @staticmethod
    def createProduct(session, product_dataclass: ProductBase):
        series = Series.as_unique(session, name=product_dataclass.series)
        manufacturer = Company.as_unique(session, name=product_dataclass.manufacturer)
        category = Category.as_unique(session, name=product_dataclass.category)
        releaser = Company.as_unique(session, name=product_dataclass.releaser)
        distributer = Company.as_unique(session, name=product_dataclass.distributer)

        paintworks = Paintwork.multiple_as_unique(session, product_dataclass.paintworks)
        sculptors = Sculptor.multiple_as_unique(session, product_dataclass.sculptors)

        images = ProductOfficialImage.create_image_list(product_dataclass.images)

        release_infos = []
        for release in product_dataclass.release_infos:
            release: Release
            release_info = ReleaseToProductReleaseInfoModelAdapter(release)
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
            # relationship
            release_infos=release_infos,
            sculptors=sculptors,
            paintworks=paintworks,
            official_images=images
        )

        return product

    @staticmethod
    def updateProduct(product_dataclass: ProductBase, product_model: Product):
        if len(product_dataclass.prices) != len(product_dataclass.release_dates):
            raise ValueError("Please ensure the length of .prices and release_dates are same.")

        is_delay = len(product_model.release_infos) == len(product_dataclass.release_dates)

        if is_delay:
            product_model.release_infos[0].postpone_release_date_to(product_dataclass.release_dates[-1])

        if not is_delay:
            new_release_dates = product_dataclass.release_dates[len(product_model.release_infos)-1:]
            new_prices = product_dataclass.prices[len(product_model.release_infos)-1:]

            for date, price in zip(new_release_dates, new_prices):
                product_model.release_infos.append(
                    ProductReleaseInfo(
                        price=price,
                        initial_release_date=date
                    )
                )

        product_model.save()
        return product_model
