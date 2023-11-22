from dataclasses import dataclass


@dataclass
class Element:
    name: str
    index: int
    length: float
    type: str
