from dataclasses import dataclass

from lat2db.model.element import Element

from typing import Optional

@dataclass
class Drift(Element):
    name: Optional[str] = None
    index: Optional[int] = None
    length: float = 0.0
    type: str = "Drift"