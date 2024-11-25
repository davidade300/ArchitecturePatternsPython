from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import registry
from architecture_patterns_python.model import (
    OrderLine,
)  # the ORM imports (depends/knows about) the domail model, not the other way around

mapper_registry = registry()

metadata = MetaData()

order_lines = Table(  # We define our databases tables and columns by using SQLAlchemy's abstractions
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)


# When called, the mapper function does its magic to bind our domain model classes
# to the various tables we defined
def start_mappers():
    # lines_mapper = mapper_registry.map_declaratively(model.OrderLine, order_lines)
    mapper_registry.map_imperatively(OrderLine, order_lines)
