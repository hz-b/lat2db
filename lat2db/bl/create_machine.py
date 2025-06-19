import logging
from typing import Dict, Callable

from ..model.geometric_info import GeometricInfo
from ..model.lattice_elements.beam_position_monitor import BeamPositionMonitor
from ..model.lattice_elements.bending import Bending
from ..model.lattice_elements.cavity import Cavity
from ..model.lattice_elements.drift import Drift
from ..model.lattice_elements.marker import Marker
from ..model.lattice_elements.quadrupole import Quadrupole
from ..model.lattice_elements.sextupole import Sextupole
from ..model.lattice_elements.steerer import Steerer
from ..model.machine import (
    extact_version_from_lattice,
    extract_physics_info_from_lattice,
    Machine,
)


logger = logging.getLogger("lat2db")


factory_dict_default = {
    "Drift": Drift,
    "Marker": Marker,
    "Sextupole": Sextupole,
    "Steerer": Steerer,
    "Bending": Bending,
    "Quadrupole": Quadrupole,
    "Bpm": BeamPositionMonitor,
    "Cavity": Cavity,
    "Horizontalsteerer": None,
    "Verticalsteerer": None,
}


def create_machine(lat, factory_dict: Dict[str, Callable] = None):
    factory_dict = factory_dict or factory_dict_default
    elms = [
        process_element(standardise_element_info(row_), factory_dict=factory_dict)
        for row_ in lat.elements
    ]
    # Todo: how to hande elements we are not processing further ...
    # shall one add a place holder
    elms = [elm for elm in elms if elm is not None]
    machine = Machine(
        sequences=[elms],
        version=extact_version_from_lattice(
            lat.lattice_standard_metadata.lattice_version
        ),
        phyics_info=extract_physics_info_from_lattice(lat.properties.physics.energy),
        geometric_info=GeometricInfo(is_ring=lat.properties.geometric.is_ring),
        name=lat.lattice_standard_metadata.machine_name,
        closed=lat.lattice_standard_metadata.closed,
    )
    return machine


def process_element(elem_info: Dict, *, factory_dict):
    type_class = factory_dict[elem_info["type"]]
    if not type_class:
        return None
    try:
        r = type_class(**elem_info)
    except Exception as exc:
        pass
        raise exc
    return r


def standardise_element_info(elem_info: Dict, *, copy: bool = True):
    # iterate through each row in lat.elements

    # make a copy of the row so that changes don't affect original data
    if copy:
        elem_info = elem_info.copy()

    # print the row
    logger.debug("elem_info= %s", elem_info)

    # revamp parameters as required for the dataclasses
    elem_info.setdefault("length", elem_info.pop("L", 0e0))  # rename "L" to "length"
    type_name = elem_info["type"]
    if type_name in ["Quadrupole", "Sextupole"]:
        if "K" in elem_info.keys():
            elem_info["main_multipole_strength"] = elem_info.pop("K")
    elif type_name == "Bending":
        if "K" in elem_info.keys():
            elem_info["quadrupole_strength"] = elem_info.pop("K")
    elif type_name == "Steerer":
        if "K" in elem_info.keys():
            raise AssertionError("Did not expect K in steerer data")
    if type_name in ["Bending", "Quadrupole", "Sextupole", "Steerer"]:
        # Integration info now in a separate part
        if "N" in elem_info.keys():
            elem_info["integration_parameters"] = dict(
                n_slices=elem_info.pop("N"), symplectic_order=elem_info.pop("Method")
            )
    if type_name == "Cavity":
        elem_info["frequency"] = elem_info.pop(
            "Frequency", 0e0
        )  # rename "Frequency" to "frequency"
        elem_info["voltage"] = elem_info.pop(
            "Voltage", 0e0
        )  # rename "Voltage" to "voltage"
        elem_info["harmonic_number"] = elem_info.pop(
            "Harmonicnumber", 0e0
        )  # rename "HarmonicNumber" to "harmonic_number"
    else:
        pass  # do nothing if type_name is not recognized

    if type_name == "Bending":
        elem_info.setdefault(
            "bending_angle", elem_info.pop("T", 0e0)
        )  # rename "T" to "bending_angle"
        elem_info.setdefault(
            "entry_angle", elem_info.pop("T1", 0e0)
        )  # rename "T1" to "entry_angle"
        elem_info.setdefault(
            "exit_angle", elem_info.pop("T2", 0e0)
        )  # rename "T2" to "exit_angle"

    return elem_info


__all__ = ["create_machine"]
