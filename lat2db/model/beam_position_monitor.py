from dataclasses import dataclass

from lat2db.model.element import Element

from typing import Optional
from typing import Sequence

@dataclass
class BeamPositionMonitor(Element):
    passmethod: Optional[str] = None

    md: Optional[object] = None
    tags: Optional[Sequence[str]] = None