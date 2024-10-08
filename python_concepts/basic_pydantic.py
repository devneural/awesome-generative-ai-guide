from datetime import datetime
from typing import Tuple

from pydantic import BaseModel

class Delivery(BaseModel):
    timestamp: datetime
    dimensions: Tuple[int, int]


m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
print(repr(m.timestamp))
print(m.dimensions)


"""
Pydantic helps you ensure that the data you’re working with conforms to the types and 
constraints you expect, which is especially useful in data-intensive applications.
"""