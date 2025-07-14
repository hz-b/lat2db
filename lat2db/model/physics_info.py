from pydantic.dataclasses import dataclass

from pydantic import Field

from lat2db.model.energy import Energy


@dataclass
class PhysicsInfo:
    energy: Energy = Field(default=None)
