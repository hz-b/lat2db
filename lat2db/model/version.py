from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Version:
    major: int
    minor: int
    level: int
    effective_from: datetime
    effective_to: Optional[datetime] = None
