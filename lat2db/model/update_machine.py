from typing import Optional, List

from pydantic import BaseModel, Field

from lat2db.model.beam_position_monitor import BeamPositionMonitor
from lat2db.model.bending import Bending
from lat2db.model.cavity import Cavity
from lat2db.model.drift import Drift
from lat2db.model.geometric_info import GeometricInfo
from lat2db.model.marker import Marker
from lat2db.model.physics_info import PhysicsInfo
from lat2db.model.quadrupole import Quadrupole
from lat2db.model.sequencer import Sequencer
from lat2db.model.sextupole import Sextupole
from lat2db.model.version import Version


class MachineUpdate(BaseModel):
    sequences: Optional[List[Sequencer]]
    quadrupoles: Optional[List[Quadrupole]]
    sextupoles: Optional[List[Sextupole]]
    drifts: Optional[List[Drift]]
    bendings: Optional[List[Bending]]
    markers: Optional[List[Marker]]
    beam_position_monitors: Optional[List[BeamPositionMonitor]]
    cavities: Optional[List[Cavity]]
    name: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "MLS",
            }
        }
