import logging
from typing import Dict, Callable, Union

from ..model.geometric_info import GeometricInfo
from ..model.lattice_elements.beam_position_monitor import BeamPositionMonitor
from ..model.lattice_elements.bending import Bending
from ..model.lattice_elements.cavity import Cavity
from ..model.lattice_elements.drift import Drift
from ..model.lattice_elements.element import Element, ElementTypeNames
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

_elm_t_nams = ElementTypeNames

factory_dict_default = {
    _elm_t_nams.marker.value: Marker,
    _elm_t_nams.bpm.value: BeamPositionMonitor,
    _elm_t_nams.drift.value: Drift,
    _elm_t_nams.bending.value: Bending,
    _elm_t_nams.quadrupole.value: Quadrupole,
    _elm_t_nams.sextupole.value: Sextupole,
    _elm_t_nams.steerer.value: Steerer,
    "Horizontalsteerer": None,
    "Verticalsteerer": None,
    _elm_t_nams.cavity.value: Cavity,
}


def create_machine(lat, factory_dict: Dict[str, Callable] = None) -> Machine:
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


def process_element(elem_info: Dict, *, factory_dict) -> Element:
    type_class = factory_dict[elem_info["type"]]
    if not type_class:
        return None
    try:
        r = type_class(**elem_info)
    except Exception as exc:
        pass
        raise exc
    return r


def standardise_element_info(
    elem_info: Dict[str, Union[str, int, float]], *, copy: bool = True
) -> Dict[str, Union[str, int, float, Dict[str, int]]]:

    if copy:
        res = elem_info.copy()
    logger.debug("elem_info= %s", res)

    # revamp parameters as required for the dataclasses
    res["length"] = res.pop("L", 0e0)

    type_name = res["type"]
    # address main strength
    if type_name in [_elm_t_nams.quadrupole.value, _elm_t_nams.sextupole.value]:
        if "K" in res.keys():
            res["main_multipole_strength"] = res.pop("K")
    elif type_name == _elm_t_nams.bending.value:
        if "K" in res.keys():
            res["quadrupole_strength"] = res.pop("K")
    elif type_name == _elm_t_nams.steerer.value:
        if "K" in res.keys():
            raise AssertionError("Did not expect K in steerer data")

    if type_name in [
        _elm_t_nams.bending.value,
        _elm_t_nams.quadrupole.value,
        _elm_t_nams.sextupole.value,
        _elm_t_nams.steerer.value,
    ]:
        # Integration info now in a separate dataclass
        if "N" in res.keys():
            res["integration_parameters"] = dict(
                n_slices=int(res.pop("N")),
                symplectic_order=int(res.pop("Method")),
            )

    # renaming for specific parts
    if type_name == _elm_t_nams.bending.value:
        res["bending_angle"] = res.pop("T", 0e0)
        res["entry_angle"] = res.pop("T1", 0e0)
        res["exit_angle"] = res.pop("T2", 0e0)

    if type_name == _elm_t_nams.cavity.value:
        res["frequency"] = res.pop("Frequency", 0e0)
        res["voltage"] = res.pop("Voltage", 0e0)  # rename "Voltage" to "voltage"
        res["harmonic_number"] = res.pop("Harmonicnumber", 0e0)
    else:
        pass  # do nothing if type_name is not recognized

    return res


__all__ = ["create_machine"]
