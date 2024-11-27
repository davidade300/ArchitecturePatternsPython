from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, clear_mappers
from architecture_patterns_python import repository, model
import pytest
from architecture_patterns_python.orm import metadata, start_mappers


@pytest.fixture(scope="function")
def session():
    clear_mappers()
    start_mappers()

    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )

    metadata.create_all(engine, checkfirst=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


def test_orderline_mapper_can_load_lines(session):
    session.execute(
        text(
            "INSERT INTO order_lines (orderid, sku, qty) VALUES ('order1', 'RED-CHAIR', 12),('order1', 'RED-TABLE', 13),('order2', 'BLUE-LIPSTICK', 14);"
        )
    )

    session.commit()

    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]

    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)

    session.add(new_line)

    session.commit()

    rows = list(
        session.execute(text("SELECT orderid, sku, qty FROM 'order_lines';"))
    )

    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]


def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        text("SELECT reference, sku, _purchased_quantity, eta FROM 'batches' ;")
    )

    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]
