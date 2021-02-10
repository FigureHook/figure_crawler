from src.Models import (Category, Company, Paintwork, Product,
                        ProductOfficialImage, ProductReleaseInfo, Sculptor,
                        Series)

from .product import ProductBase


__all__ = ["ProductModelFactory"]


class ProductModelFactory:
    @staticmethod
    def createProduct(session, product_dataclass: ProductBase):
        if len(product_dataclass.prices) != len(product_dataclass.release_dates):
            raise ValueError("Please ensure the length of .prices and release_dates are same.")

        series = Series.as_unique(session, name=product_dataclass.series)
        manufacturer = Company.as_unique(session, name=product_dataclass.manufacturer)
        category = Category.as_unique(session, name=product_dataclass.category)
        releaser = Company.as_unique(session, name=product_dataclass.releaser)
        distributer = Company.as_unique(session, name=product_dataclass.distributer)

        release_infos = [
            ProductReleaseInfo(
                price=price,
                initial_release_date=date
            )
            for price, date
            in zip(product_dataclass.prices, product_dataclass.release_dates)
        ]

        paintworks = [
            Paintwork.as_unique(session, name=paintwork)
            for paintwork in product_dataclass.paintworks
        ]

        sculptors = [
            Sculptor.as_unique(session, name=sculptor)
            for sculptor in product_dataclass.sculptors
        ]

        images = [
            ProductOfficialImage(url=image)
            for image in product_dataclass.images
        ]

        product = Product(
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
