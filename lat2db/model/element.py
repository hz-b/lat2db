from dataclasses import dataclass
from typing import Optional


@dataclass
class Element:
    #: actually an identifier
    name: str
    index: int
    #: in meter
    length: float
    #: to be interpreted by the factories building a lattice from the database
    type: str
    #: everythng describing the element itself beyond to the information given
    #: in the fields above
    # element_configuration: object


__all__ = ["Element"]
