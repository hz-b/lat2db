from dataclasses import dataclass


@dataclass
class Energy:
    egu: str
    name: str
    value: float