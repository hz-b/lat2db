from dataclasses import dataclass

@dataclass
class Element:
    #: actually an identifier
    name: str
    index: int
    #: in meter
    length: float
    #: to be interpreted by the factories building a lattice from the database
    type: str

__all__ = ["Element"]