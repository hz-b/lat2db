from dataclasses import dataclass
from typing import Sequence


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
    md:  object
    # tags are given by specific lattice developers to later sort/filter/categorised/group or wild card search their
    # elements
    tags: Sequence[str]


__all__ = ["Element"]
