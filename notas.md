# This repo contains the app developed in the "architecture Patterns with Python" book

## Value Object Pattern

- Whenever we have a business concept that has data but no identity, we often choose to represent it using the "Value Object Pattern". A Value Object is any domain object that
is uniquely identified by the data it holds: we usually make them immutable:

```Python
from dataclasses import dataclass
from typing import NamedTuple
from collections import namedtuple

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str

class Money(NamedTuple):
    currency: str
    value: int

Line = namedtuple("Line",["sku", "qty"])

def test_equality():
    assert Money("gbp", 10) == Money("gbp", 10)
    assert Name("Harry", "percival") != Name("bob", "gregory")
```
