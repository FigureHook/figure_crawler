from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Model

metadata = Model.metadata
# association table
product_sculptor_table = Table(
    "product_sculptor", metadata,
    Column("product_id", Integer, ForeignKey("product.id", ondelete="CASCADE")),
    Column("sculptor_id", Integer, ForeignKey("sculptor.id", ondelete="CASCADE"))
)

product_paintwork_table = Table(
    "product_paintwork", metadata,
    Column("product_id", Integer, ForeignKey("product.id", ondelete="CASCADE")),
    Column("paintwork_id", Integer, ForeignKey("paintwork.id", ondelete="CASCADE"))
)
