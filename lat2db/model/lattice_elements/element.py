import enum
from typing import Sequence, Optional

from pydantic import BaseModel, Field


class Element(BaseModel):
    #: actually an identifier
    name: str
    index: int
    #: in meter
    length: float
    #: to be interpreted by the factories building a lattice from the database
    type: str
    #: everything describing the element itself beyond to the information given
    #: in the fields above
    # element_configuration: object
    # tags are given by specific lattice developers to later sort/filter/categorised/group or wild card search their
    # elements
    tags: Optional[Sequence[str]] = Field(default_factory=lambda: None)


__all__ = ["Element"]


class ElementTypeNames(enum.Enum):
    marker = "Marker"
    bpm = "Bpm"
    drift = "Drift"
    bending = "Bending"
    quadrupole = "Quadrupole"
    sextupole = "Sextupole"
    steerer = "Steerer"
    cavity = "Cavity"
    horizontal_steerer = "HorizontalSteerer"
    vertical_steerer = "VerticalSteerer"
