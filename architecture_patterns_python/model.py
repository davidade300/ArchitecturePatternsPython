from dataclasses import dataclass
from datetime import date
from typing import List, NewType

Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)


# Whenever we have a business concept that has data but no identity, we often choose to
# represent it using the "Value Object Pattern". A Value Object is any domain object that
# is uniquely identified by the data it holds; we usually make them immutable:
@dataclass(frozen=True)
class OrderLine:
    """
    A Value object can be defined as:
    Any object that is identified only by its data and doesn't have a long-lived identity,
    (in contrast, the term entity is used to describe a domain object that has long-lived identity )
    """

    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(
        self, ref: Reference, sku: Sku, qty: Quantity, eta: date | None
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: set[OrderLine] = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    # métodos que são propriedades podem ser chamados sem o ()
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    # __eq__ defines the behavior of the class for the "==" operator
    def __eq__(self, other) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    # __hash__ defines the behavior of objects when you add them to sets or use them as dict keys
    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


class OutOfStock(Exception):
    pass


# this is a domain service. A domain service represents a business concept or prcess,
# whereas a service-layer service represents a use case for your application.
# Often the service layer weill call a domain service
def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
