import architecture_patterns_python.model as model
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, clear_mappers
from architecture_patterns_python.orm import metadata, start_mappers
import architecture_patterns_python.repository as repository


@pytest.fixture(scope="session")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    with Session(in_memory_db) as session:
        yield session
    clear_mappers()


def test_orderline_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES (order1, RED-CHAIR, 12),(order1, RED-TABLE, 13),(order2, BLUE-LIPSTICK, 14)"
    )

    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]

    session.commit()

    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(
        session.execute('--sql SELECT orderid, sku, qtry FROM "order_lines"')
    )

    assert rows == [("oder1", "DECORATIVE-WIDGET", 12)]


def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        "SELECT reference, sku, _purchased_quantity, eta FROM 'batches'"
    )

    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]
