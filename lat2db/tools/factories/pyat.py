"""build sequence of accelerator toolbox lattice elements
"""
import enum
import logging
import math
from functools import partial

import at
import jsons
import numpy as np

from ...model.bending import Bending
from ...model.cavity import Cavity
from ...model.element import Element
from ...model.quadrupole import Quadrupole
from ...model.sextupole import Sextupole

logger = logging.getLogger("lat2db")
__all__ = ["factory"]


def factory(expr: dict):
    """
    Args:
        energy: energy of the accelerator: only used by the cavities
    """

    # energy_prop = expr["physics_info"]["energy"]
    # assert energy_prop["egu"] == "GeV"
    # assert energy_prop["name"] == "energy"
    energy = 1.7e9  # float(energy_prop["value"]) * 1e9

    factory_dict = factory_dict_default.copy()
    factory_dict["RFCavity"] = partial(instaniate_cavity, energy=energy)
    seq_expr = expr["sequences"]
    elements = [instantiate_element(e, factory_dict=factory_dict) for e in seq_expr]
    return elements


def instantiate_element(prop, *, factory_dict):
    type_ = prop["type"]
    return factory_dict[type_](prop)


def instantiate_marker(prop: dict):
    #: Todo re
    return at.Marker(prop["name"], length=0)


def instantiate_monitor(prop: dict):
    #: Todo re
    return at.Monitor(prop["name"], length=0)


def instantiate_drift(prop: dict):
    return at.Drift(prop["name"], length=prop["length"])


def instantiate_bending(prop: dict):
    """


    Todo:
        reference to definition
        Check in which units angles are stored in lat2d
        Check in which units angles are used by at

        Check what the definition of h is
    """
    h = 0.0
    p = jsons.load(prop, Bending)
    #: Todo: should irho be checked then
    return at.Dipole(
        p.name,
        h=h,
        ExitAngle=p.exitangle,
        EntranceAngle=p.entranceangle,
        bending_angle=p.bending_angle,
        k=0.0,
        length=p.length,
        FringeInt2=getattr(p, 'fringeInt2', 0.0),
        FringeInt1=getattr(p, 'fringeInt1', 0.0),
        FullGap=getattr(p, 'fullgap', 0.0),
        PolynomA=p.element_configuration.magnetic_element.coeffs.normal_coefficients,
        PolynomB=p.element_configuration.magnetic_element.coeffs.skew_coefficients
    )


def instanitate_quadrupole(prop: dict):
    """
    Todo:
    check which convention k follows
    """
    logger.debug(f"Quadrupole {prop=}")
    try:
        p = jsons.load(prop, Quadrupole)
    except jsons.exceptions.DeserializationError:
        logger.error(f"Could not load Quadrupole using properties {prop}")
        raise
    k = p.element_configuration.magnetic_element.main_multipole_strength
    r = at.Quadrupole(p.name, length=p.length, k=k,
                      PolynomA=p.element_configuration.magnetic_element.coeffs.normal_coefficients,
                      PolynomB=p.element_configuration.magnetic_element.coeffs.skew_coefficients)
    assert np.isfinite(r.K)
    return r


#


def instanitate_sextupole(prop: dict):
    """
    Todo:
        check which convention h follows?
    """
    # h = prop.main_multipole_strength
    logger.debug(f"Sextupole {prop=}")
    try:
        p = jsons.load(prop, Sextupole)
    except jsons.exceptions.DeserializationError:
        logger.error(f"Could not load Sextupole using properties {prop}")
        raise
    r = at.Sextupole(p.name, p.length, PolynomA=p.element_configuration.magnetic_element.coeffs.normal_coefficients,
                     PolynomB=p.element_configuration.magnetic_element.coeffs.skew_coefficients, Corrector=p.tags[0],
                     KickAngle=[p.element_configuration.kickangle.x, p.element_configuration.kickangle.y])
    assert np.isfinite(r.H)
    return r


class SteererOrientation(enum.Enum):
    horizontal = "horizontal"
    vertical = "vertical"


def instanitate_steerer(prop: Element, *, orientation: SteererOrientation):
    """
    Todo:
        What is test?
        What is kick angle ?
    """
    orientation = SteererOrientation(orientation)
    if orientation == SteererOrientation.horizontal:
        test = 0
    elif orientation == SteererOrientation.horizontal:
        test = math.pi / 2
    else:
        raise AssertionError("Should not end up here")

    return at.Corrector(prop.name, length=prop.length, test=test, kick_angle=[0, 0])


def instaniate_cavity(prop: dict, *, energy):
    """Instanitate a heavily broken element

    Using voltage is inconsistent with using K values for quad
    Energy is a property of the beam not of the cavity

    Todo:
        check what unit the frequencies in
        check why voltage are 0

    """
    logger.debug(f"cavity property {prop=}")
    p = jsons.load(prop, Cavity)
    voltage = p.element_configuration.voltage

    energy = energy
    return at.RFCavity(
        p.name,
        length=p.length,
        frequency=p.element_configuration.frequency,
        harmonic_number=p.harmonic_number,
        voltage=voltage,
        energy=energy,
    )


factory_dict_default = dict(
    Marker=instantiate_marker,
    Monitor=instantiate_monitor,
    Drift=instantiate_drift,
    Dipole=instantiate_bending,
    Quadrupole=instanitate_quadrupole,
    Sextupole=instanitate_sextupole
)

# due to historic reasons: need to get the that cleaned away
factory_dict_default["Monitor"] = factory_dict_default["Monitor"]
