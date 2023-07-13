from dataclasses import dataclass

from pydantic import Field

from src.model.energy import Energy


@dataclass
class PhysicsInfo:
    energy: Energy = Field(default=None)
