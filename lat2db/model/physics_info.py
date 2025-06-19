from pydantic.dataclasses import dataclass
from pydantic import Field

from .energy import Energy


@dataclass
class PhysicsInfo:
    energy: Energy = Field(default=None)
