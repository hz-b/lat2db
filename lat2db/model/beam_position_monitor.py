from dataclasses import dataclass

from lat2db.model.element import Element

from typing import Optional

@dataclass
class BeamPositionMonitor(Element):
    passmethod: Optional[str] = None
