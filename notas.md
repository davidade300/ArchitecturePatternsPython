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

## Repository pattern

- ~~I still dont understand it so im writing about it to see if that changes anything~~;

- The Reposityor Pattern is an abstraction over persistent storage:
  - It is an abstraction of the data layer and a way of centralising the handling of the domain objects;
  - One way to think of it is to pretend that all of our data is in memory. Even though our objects are in memory, we need to put them somewhere so we can find them again. Our in-memory data would let us add new objects. Because the objects are in memory, we never need to call a .save() method, we just fetch the object we care about and modify it in memory.
- You will probably end up having to write a few more lines of code in our repository class each time a new domain object that you want to retrieve is added, but in return you get a simple abstraction over the storage layer, which you control. The Repository Pattern would make it easy to make fundamental changes to the way things are stored.
