import uuid
from pydantic.dataclasses import dataclass
from typing import List

from pydantic import Field
from datetime import datetime

from lat2db.model.beam_position_monitor import BeamPositionMonitor
from lat2db.model.bending import Bending
from lat2db.model.cavity import Cavity
from lat2db.model.drift import Drift
from lat2db.model.horizontal_steerer import HorizontalSteerer
from lat2db.model.marker import Marker
from lat2db.model.physics_info import PhysicsInfo
from lat2db.model.quadrupole import Quadrupole
from lat2db.model.sequencer import Sequencer
from lat2db.model.sextupole import Sextupole
from lat2db.model.version import Version
from lat2db.model.vertical_steerer import VerticalSteerer
from lat2db.model.energy import Energy
from lat2db.model.geometric_info import GeometricInfo


@dataclass()
class Machine():
    sequences: List[Sequencer] = Field(default_factory=list)
    quadrupoles: List[Quadrupole] = Field(default_factory=list)
    sextupoles: List[Sextupole] = Field(default_factory=list)
    drifts: List[Drift] = Field(default_factory=list)
    bendings: List[Bending] = Field(default_factory=list)
    markers: List[Marker] = Field(default_factory=list)
    horizontal_steerers: List[HorizontalSteerer] = Field(default_factory=list)
    vertical_steerers: List[VerticalSteerer] = Field(default_factory=list)
    beam_position_monitors: List[BeamPositionMonitor] = Field(default_factory=list)
    cavities: List[Cavity] = Field(default_factory=list)
    version: Version = Field(default=None)
    geometric_info: GeometricInfo = Field(default=None)
    physics_info: PhysicsInfo = Field(default=None)
    name: str = "unknown"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    def add_drift(self, drift):
        self.drifts.append(drift)

    def add_bending(self, bending):
        self.bendings.append(bending)

    def add_sextupole(self, sextupole):
        self.sextupoles.append(sextupole)

    def add_quadrupole(self, quadrupole):
        self.quadrupoles.append(quadrupole)

    def add_marker(self, marker):
        self.markers.append(marker)

    def add_horizontal_steerer(self, horizontal_steerer):
        self.horizontal_steerers.append(horizontal_steerer)

    def add_vertical_steerer(self, vertical_steerer):
        self.vertical_steerers.append(vertical_steerer)

    def add_beam_position_monitor(self, beam_position_monitor):
        self.beam_position_monitors.append(beam_position_monitor)

    def add_cavity(self, cavity):
        self.cavities.append(cavity)

    def add_to_sequence(self, sequence_item):
        self.sequences.append(sequence_item)

    def set_base_parameters(self, lat):
        self.name = lat.lattice_standard_metadata.machine_name
        lat_version = lat.lattice_standard_metadata.lattice_version
        lat_energy = lat.properties.physics.energy
        self.version = Version(lat_version.major, lat_version.minor, lat_version.patch_level, datetime.utcnow())
        self.physics_info = PhysicsInfo(Energy(lat_energy.egu, lat_energy.name, lat_energy.value))
        self.geometric_info = GeometricInfo(lat.properties.geometric.is_ring)
    class Config:
        arbitrary_types_allowed: True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "name of machine",
                "sequences": [],
                "quadrupoles":[],
                "sextupoles": [],
                "drifts": [],
                "bendings": [],
                "markers": [],
                "horizontal_steerers": [],
                "vertical_steerers": [],
                "beam_position_monitors": [],
                "cavities": [],
                "version": "",
                "geometric_info": "",
                "physics_info": ""
            }
        }