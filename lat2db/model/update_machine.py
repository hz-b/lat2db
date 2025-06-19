from typing import Optional, List

from pydantic import BaseModel

from .lattice_elements.beam_position_monitor import BeamPositionMonitor
from .lattice_elements.bending import Bending
from .lattice_elements.cavity import Cavity
from .lattice_elements.drift import Drift
from .lattice_elements.marker import Marker
from lat2db.model.sequencer import Sequencer
from .lattice_elements.quadrupole import Quadrupole
from .lattice_elements.sextupole import Sextupole


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
