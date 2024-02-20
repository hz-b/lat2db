from dataclasses import dataclass

from lat2db.model.element import Element


@dataclass
class Cavity(Element):
    name: str = ""
    index: int = 0
    length: float = 0
    type: str = "Cavity"
    frequency: float=0
    harmonic_number: int=0
    voltage: float=0
    phase: float = 0.0

