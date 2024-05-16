from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Version(BaseModel):
    major: int
    minor: int
    level: int
    effective_from: datetime
    effective_to: Optional[datetime] = None
