from dataclasses import dataclass

from lat2db.model.element import Element
from typing import Optional


@dataclass
class Marker(Element):
    """A virtual beam position monitor

    Used to get data at any point within the machine
    """
    name: Optional[str] = None
    index: Optional[int] = None
    length: float = 0.0
    type: str = "Marker"
