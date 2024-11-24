from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship  # noqa: F401
import architecture_patterns_python.model as model  # the ORM imports (depends/knows about) the domail model, not the other way around

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
    lines_mapper = mapper(model.OrderLine, order_lines)
