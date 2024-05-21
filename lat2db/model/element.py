from typing import Sequence, Optional

from pydantic import BaseModel


class Element(BaseModel):
    #: actually an identifier
    name: Optional[str]
    index: Optional[int]
    #: in meter
    length: Optional[float]
    #: to be interpreted by the factories building a lattice from the database
    type: Optional[str]
    #: everythng describing the element itself beyond to the information given
    #: in the fields above
    # element_configuration: object
    # tags are given by specific lattice developers to later sort/filter/categorised/group or wild card search their
    # elements
    passmethod: Optional[str]
    tags: Optional[Sequence[str]]


__all__ = ["Element"]
