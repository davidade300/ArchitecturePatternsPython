import abc

from architecture_patterns_python.model import Batch


# To me, it seems that this work exactly like a interface in Java
class AbstractRepository(abc.ABC):
    """
    @abc.abstractmethod is one of the only things that makes ABCs actually "work" in Python.
    Python will refuse to let you instantiate a class that does not implement all the abstractmethods
    defined in its parent class. Besides that, the NotImplementError is not really necessary or sufficient.
    Abstract methods can have real behavior that subclasses can call out to.
    """

    @abc.abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch: Batch):  # TODO: check need to remove the hint later
        self.session.add(batch)
        # self.session.execute(
        #     text(
        #         "INSERT INTO batches (reference, sku, _purchased_quantity, eta) VALUES (); "
        #     )
        # )

    def get(self, reference) -> Batch:  # TODO check need to remove return type
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(Batch).all()
