from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Model

metadata = Model.metadata
# association table
product_sculptor_table = Table(
    "product_sculptor", metadata,
    Column("prodcut_id", Integer, ForeignKey("product.id")),
    Column("sculptor_id", Integer, ForeignKey("sculptor.id"))
)

product_paintwork_table = Table(
    "product_paintwork", metadata,
    Column("prodcut_id", Integer, ForeignKey("product.id")),
    Column("paintwork_id", Integer, ForeignKey("paintwork.id"))
)
