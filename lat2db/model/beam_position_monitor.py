from dataclasses import dataclass

from lat2db.model.element import Element


@dataclass
class BeamPositionMonitor(Element):
    name: str = ""
    index: int = 0
    length: float = 0.0
    type: str = "Bpm"