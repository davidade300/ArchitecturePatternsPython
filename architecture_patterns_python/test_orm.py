from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from architecture_patterns_python.model import OrderLine
import pytest
from architecture_patterns_python.orm import metadata, start_mappers


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite+pysqlite:///C:\\Users\\iader\\Desktop\\Estudos\\Livros\\Architecture_patterns_python\\architecture_patterns_python\\database.db"
    )
    metadata.create_all(engine)
    start_mappers()
    Session = sessionmaker(bind=engine)
    return Session()


def test_orderline_mapper_can_load_lines(session):
    engine = session.bind
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO order_lines (orderid, sku, qty) VALUES ('order1', 'RED-CHAIR', 12),('order1', 'RED-TABLE', 13),('order2', 'BLUE-LIPSTICK', 14);"
            )
        )

        conn.commit()

    expected = [
        OrderLine("order1", "RED-CHAIR", 12),
        OrderLine("order1", "RED-TABLE", 13),
        OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]

    assert session.query(OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    # engine = session.bind
    new_line = OrderLine("order1", "DECORATIVE-WIDGET", 12)

    session.add(new_line)
    session.commit()
    # with engine.connect() as conn:
    #    conn.add(new_line)
    #    conn.commit()

    rows = list(
        session.execute(text("SELECT orderid, sku, qty FROM 'order_lines';"))
    )

    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]


# def test_repository_can_save_a_batch(session):
#     batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

#     repo = repository.SqlAlchemyRepository(session)
#     repo.add(batch)
#     session.commit()

#     rows = session.execute(
#         "SELECT reference, sku, _purchased_quantity, eta FROM 'batches'"
#     )

#     assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]
