from dataclasses import dataclass

from src.model.element import Element


@dataclass
class Cavity(Element):
    frequency: float
    harmonic_number: int
    voltage: float
    phase: float = 0.0

