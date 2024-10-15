"""Dataclasses for describing a lattice

"""
import time
from typing import List, Union

from attr import dataclass



@dataclass
class PhysicsParameter:
    """
    Todo:
       have a look into pint
    """

    name: str
    value: float
    #: engineering unit ...
    egu: str

    def to_dict(self):
        return dict(name=self.name, value=self.value, egu=self.egu)


@dataclass
class LatticePhysicsProperties:
    """

    Todo:
       * Review missing parameters
    """

    #: energy of the setup. define eng
    energy: PhysicsParameter

    def to_dict(self):
        return dict(energy=self.energy.to_dict())


@dataclass
class LatticeGeometryProperties:
    #: is it a linac type or a ring type
    is_ring: bool

    def to_dict(self):
        return dict(is_ring=self.is_ring)


@dataclass
class VersionInfo:
    major: int
    minor: int
    patch_level: int

    def to_dict(self):
        return dict(major=self.major, minor=self.minor, patch_level=self.patch_level)


@dataclass
class StorageFormatMetadata:
    version: VersionInfo

    def to_dict(self):
        return dict(version=self.version.to_dict())


@dataclass
class LatticeMetadata:
    machine_name: str
    lattice_version: VersionInfo
    closed: bool

    def to_dict(self):
        return dict(
            machine_name=self.machine_name,
            lattice_version=self.lattice_version.to_dict(),
            closed=self.closed
        )


@dataclass
class LatticeProperties:
    physics: LatticePhysicsProperties
    geometric: LatticeGeometryProperties

    def to_dict(self):
        return dict(
            physics=self.physics.to_dict(),
            geometric=self.geometric.to_dict(),
        )


@dataclass
class Lattice:
    """

    Todo:
        Do we need sublattices?
        E.g. BESSY II as a top lattice with booster
        and storage ring as sublattices
    """

    properties: LatticeProperties
    lattice_standard_metadata: LatticeMetadata
    storage_format: StorageFormatMetadata
    user_meta_data: dict
    #: Unix timestamp
    #: not a windows timestamp or a mac time stamp
    timestamp: time.time
    elements: List
    # [Union[ed.Drift|ed.Marker|ed.MultipoleKick|ed.Sextupole|ed.Quadrupole]]

    def to_dict(self):
        return dict(
            storage_format=self.storage_format.to_dict(),
            lattice_standard_meta_data=self.lattice_standard_metadata.to_dict(),
            user_meta_data=self.user_meta_data,
            timestamp=self.timestamp,
            properties=self.properties.to_dict(),
            elements=self.elements,
        )
