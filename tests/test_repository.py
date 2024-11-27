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


def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = list(
        session.execute(
            text(
                "SELECT reference, sku, _purchased_quantity, eta FROM 'batches' ;"
            )
        )
    )

    assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]
