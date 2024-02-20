from dataclasses import dataclass

from lat2db.model.element import Element


@dataclass
class Cavity(Element):
    #: in Hertz
    frequency: float
    harmonic_number: int
    voltage: float
    phase: float = 0.0

    name: str = ""
    index: int = 0
    length: float = 0.0
    type: str = "Cavity"

