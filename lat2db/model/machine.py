import itertools
import uuid
import datetime
from collections.abc import Iterator
from functools import cached_property
from typing import List, Sequence, TypeVar, Dict
from pydantic import Field, BaseModel
import re

from .energy import Energy
from .geometric_info import GeometricInfo
from .lattice_elements.beam_position_monitor import BeamPositionMonitor
from .lattice_elements.bending import Bending
from .lattice_elements.cavity import Cavity
from .lattice_elements.drift import Drift
from .lattice_elements.element import Element
from .lattice_elements.marker import Marker
from .lattice_elements.quadrupole import Quadrupole
from .lattice_elements.sextupole import Sextupole
from .lattice_elements.steerer import Steerer
from .physics_info import PhysicsInfo
from .version import Version
from ..tools.helper_function import filter_an_elements


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

T = TypeVar("T")


def select_elements_by_instance(elms: Iterator[Element], T) -> Sequence[T]:
    return [elm for elm in elms if isinstance(elm, T)]


def extact_version_from_lattice(lat_version) -> Version:
    return Version(
        major=lat_version.major, minor=lat_version.minor, level=lat_version.patch_level,
        effective_from=datetime.datetime.now(datetime.timezone.utc)
    )


def extract_physics_info_from_lattice(lat_energy) -> PhysicsInfo:
    r = PhysicsInfo(
        energy=Energy(egu=lat_energy.egu, name=lat_energy.name, value=lat_energy.value)
    )
    return r


def extract_geometry_info_from_lattice(lat) -> GeometricInfo:
    return GeometricInfo(is_ring=lat.properties.geometric.is_ring)


class Machine(BaseModel):
    sequences: Sequence[Sequence[Element]]
    # physics_info: PhysicsInfo
    geometric_info: GeometricInfo
    version: Version
    name: str = Field(default_factory=lambda: "unknown")
    id: str = Field(default_factory=uuid.uuid4)
    closed: bool = True

    def get_markers(self) -> Sequence[Marker]:
        return select_elements_by_instance(itertools.chain(*self.sequences), Marker)

    def get_beam_position_monitors(self) -> Sequence[BeamPositionMonitor]:
        return select_elements_by_instance(itertools.chain(*self.sequences), Marker)

    def get_drifts(self) -> Sequence[Drift]:
        return select_elements_by_instance(itertools.chain(*self.sequences), Drift)

    def get_bendings(self) -> Sequence[Bending]:
        return select_elements_by_instance(itertools.chain(*self.sequences), Bending)

    def get_quadrupoles(self) -> Sequence[Quadrupole]:
        return select_elements_by_instance(itertools.chain(*self.sequences), Quadrupole)

    def get_sextupoles(self) -> Sequence[Sextupole]:
        return select_elements_by_instance(itertools.chain(*self.sequences), Sextupole)

    def get_cavities(self) -> Sequence[Cavity]:
        return select_elements_by_instance(itertools.chain(*self.sequences), Cavity)

    def get_steerers(self) -> Sequence[Steerer]:
        return select_elements_by_instance(itertools.chain(*self.sequences), Cavity)

    def to_dict(self):
        machine = {k: v for k, v in self.dict().items() if v is not None}
        return machine

    def retrieve_element_coordinate(self, element_name):
        element = self.get_element(element_name)[0]
        start_position = 0
        for item in self.sequences:
            if item.name == element.name:
                break
            start_position += item.length

        return ElementPosition(element_name=element_name, index=element.index, start_position=start_position,
                               end_position=start_position + element.length)

    @cached_property
    def _elements_dict(self) -> Dict[str, Element]:
        return {elem.name : elem for elem in itertools.chain(*self.sequences)}

    def get_element(self, element_name) -> Element:
        """
        Todo:
            use cached property
        """
        return self._elements_dict[element_name]

    def filter_element_by_tags(self, element_name: str, tags: List[str]):
        element_list = getattr(self, element_name)
        return filter_an_elements(tags, element_list, element_name)

    class Config:
        arbitrary_types_allowed: True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "name of machine",
                "sequences": [],
                "version": "",
                "geometric_info": "",
                "physics_info": "",
                "closed" : True
            }
        }
