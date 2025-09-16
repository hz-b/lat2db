import uuid
from datetime import datetime
from typing import List
from pydantic import Field, BaseModel
import re

from lat2db.model.octupole import Octupole
from lat2db.model.steerer import Steerer
from lat2db.tools.helper_function import filter_an_elements
from lat2db.model.beam_position_monitor import BeamPositionMonitor
from lat2db.model.bending import Bending
from lat2db.model.cavity import Cavity
from lat2db.model.drift import Drift
from lat2db.model.marker import Marker
from lat2db.model.physics_info import PhysicsInfo
from lat2db.model.quadrupole import Quadrupole
from lat2db.model.sequencer import Sequencer
from lat2db.model.sextupole import Sextupole
from lat2db.model.version import Version
from lat2db.model.energy import Energy
from lat2db.model.geometric_info import GeometricInfo


class ElementPosition:
    def __init__(self, element_name: str, index: int, start_position: float, end_position: float):
        self.element_name = element_name
        self.index = index
        self.start_position = start_position
        self.end_position = end_position
        self.section = get_section_name(element_name=element_name)


def get_section_name(element_name):
    match = re.search(r'[DTKL][1-8]', element_name)
    if match:
        return match.group()
    else:
        return ""


class Machine(BaseModel):
    sequences: List[Sequencer] = Field(default_factory=list)
    quadrupoles: List[Quadrupole] = Field(default_factory=list)
    sextupoles: List[Sextupole] = Field(default_factory=list)
    octupoles: List[Octupole] = Field(default_factory=list)
    drifts: List[Drift] = Field(default_factory=list)
    bendings: List[Bending] = Field(default_factory=list)
    markers: List[Marker] = Field(default_factory=list)
    beam_position_monitors: List[BeamPositionMonitor] = Field(default_factory=list)
    cavities: List[Cavity] = Field(default_factory=list)
    steerers: List[Steerer] = Field(default_factory=list)
    name: str = "unknown"
    id: str = Field(default_factory=uuid.uuid4)
    closed: bool = True

    def add_drift(self, drift):
        self.drifts.append(drift)

    def add_bending(self, bending):
        self.bendings.append(bending)

    def add_sextupole(self, sextupole):
        self.sextupoles.append(sextupole)

    def add_octupole(self, octupole):
        self.octupoles.append(octupole)
    def add_steerer(self, steerer):
        self.steerers.append(steerer)
    def add_quadrupole(self, quadrupole):
        self.quadrupoles.append(quadrupole)

    def add_marker(self, marker):
        self.markers.append(marker)

    def add_beam_position_monitor(self, beam_position_monitor):
        self.beam_position_monitors.append(beam_position_monitor)

    def add_cavity(self, cavity):
        self.cavities.append(cavity)

    def add_to_sequence(self, sequence_item):
        self.sequences.append(sequence_item)

    def to_dict(self):
        machine = {k: v for k, v in self.dict().items() if v is not None}
        return machine

    def set_base_parameters(self, lat):
        self.name = lat.lattice_standard_metadata.machine_name
        self.closed = lat.lattice_standard_metadata.closed
        lat_version = lat.lattice_standard_metadata.lattice_version
        lat_energy = lat.properties.physics.energy
        self.version = Version(lat_version.major, lat_version.minor, lat_version.patch_level, datetime.utcnow())
        self.physics_info = PhysicsInfo(Energy(lat_energy.egu, lat_energy.name, lat_energy.value))
        self.geometric_info = GeometricInfo(lat.properties.geometric.is_ring)

    def retrieve_element_coordinate(self, element_name):
        element = self.get_element(element_name)[0]
        start_position = 0
        for item in self.sequences:
            if item.name == element.name:
                break
            start_position += item.length

        return ElementPosition(element_name=element_name, index=element.index, start_position=start_position,
                               end_position=start_position + element.length)

    def get_element(self, element_name):
        return list(filter(lambda x: x.name == element_name, self.sequences))

    def filter_element_by_tags(self, element_name: str, tags: List[str]):
        element_list = getattr(self, element_name)
        return filter_an_elements(tags, element_list, element_name)

    class Config:
        arbitrary_types_allowed: True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "name of machine",
                "sequences": [],
                "quadrupoles": [],
                "sextupoles": [],
                "drifts": [],
                "bendings": [],
                "markers": [],
                "beam_position_monitors": [],
                "cavities": [],
                "version": "",
                "geometric_info": "",
                "physics_info": "",
                "closed" : True
            }
        }
