from dataclasses import dataclass
from lat2db.model.element import Element
from typing import Optional
from typing import Sequence

@dataclass
class Marker(Element):
    """A virtual beam position monitor

    Used to get data at any point within the machine
    """
    passmethod: Optional[str] = None