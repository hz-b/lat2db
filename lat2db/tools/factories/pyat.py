"""build sequence of accelerator toolbox lattice elements
"""
import enum
import logging
import math
from functools import partial

import at
import jsons
import numpy as np
import pydantic

from ...model.bending import Bending
from ...model.cavity import Cavity
from ...model.element import Element
from ...model.magnetic_element import MagneticElement, KickAngles, AddonCorrector, MagnetAssembly
from ...model.octupole import Octupole
from ...model.quadrupole import Quadrupole
from ...model.sextupole import Sextupole
from ...model.steerer import Steerer

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
    energy = 629e6  # float(energy_prop["value"]) * 1e9

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
    p = Bending(**prop)
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
        PolynomB=p.element_configuration.magnetic_element.coeffs.normal_coefficients,
        PolynomA=p.element_configuration.magnetic_element.coeffs.skew_coefficients,
        Energy=629e6
    )


def instanitate_quadrupole(prop: dict):
    """
    Todo:
    check which convention k follows
    """
    logger.debug(f"Quadrupole {prop=}")
    try:
        # p = jsons.load(prop, Quadrupole)
        p = Quadrupole(**prop)
    except jsons.exceptions.DeserializationError:
        logger.error(f"Could not load Quadrupole using properties {prop}")
        raise
    k = p.element_configuration.magnetic_element.main_multipole_strength
    r = at.Quadrupole(p.name, length=p.length, k=k,
                      PolynomB=p.element_configuration.magnetic_element.coeffs.normal_coefficients,
                      PolynomA=p.element_configuration.magnetic_element.coeffs.skew_coefficients, Energy = 629e6)
    assert np.isfinite(r.K)
    return r


#

def instanitate_octupole(prop: dict):
    """
    Todo:
    check which convention k follows
    """
    logger.debug(f"Octupole {prop=}")
    try:
        # p = jsons.load(prop, Quadrupole)
        p = Octupole(**prop)
    except jsons.exceptions.DeserializationError:
        logger.error(f"Could not load Octupole using properties {prop}")
        raise
    k = p.element_configuration.magnetic_element.main_multipole_strength
    r = at.Octupole(p.name, length=p.length, k=k,
                      poly_b=p.element_configuration.magnetic_element.coeffs.normal_coefficients,
                      poly_a=p.element_configuration.magnetic_element.coeffs.skew_coefficients, Energy = 629e6)
    return r


def instanitate_sextupole(props: dict):
    """
    Todo:
        check which convention h follows?
    """
    # h = prop.main_multipole_strength
    logger.debug(f"Sextupole {props=}")
    try:
        # Combine props dictionary with empty tuple
        # props_combined = dict(props)  # Create a copy to avoid modifying original
        # props_combined.update(**props)  # Update with empty tuple (effectively no change)
        # p = Sextupole(**props_combined)
        p = Sextupole(**props)  #jsons.load(props, Sextupole)
    except pydantic.ValidationError as e:
        logger.error(f"Could not load Sextupole using properties {props}")
        raise e from None  # Re-raise with proper context
    r = at.Sextupole(p.name, p.length, PolynomB=p.element_configuration.magnetic_element.coeffs.normal_coefficients,
                     PolynomA=p.element_configuration.magnetic_element.coeffs.skew_coefficients, Corrector=p.tags[0],
                     KickAngle=[p.element_configuration.kickangle.x, p.element_configuration.kickangle.y], Energy = 629e6)
    assert np.isfinite(r.H)
    return r


class SteererOrientation(enum.Enum):
    horizontal = "horizontal"
    vertical = "vertical"


def instanitate_steerer(prop: Element):
    """
    Todo:
        What is test?
        What is kick angle ?
    """
    # orientation = SteererOrientation(orientation)
    # if orientation == SteererOrientation.horizontal:
    #     test = 0
    # elif orientation == SteererOrientation.horizontal:
    #     test = math.pi / 2
    # else:
    #     raise AssertionError("Should not end up here")
    kick_angle_x = prop['element_configuration']['kickangle']['x']
    kick_angle_y = prop['element_configuration']['kickangle']['y']
    return at.Corrector(prop["name"], length=prop['length'], kick_angle=[kick_angle_x, kick_angle_y])


def instaniate_cavity(prop: dict, *, energy):
    """Instanitate a heavily broken element

    Using voltage is inconsistent with using K values for quad
    Energy is a property of the beam not of the cavity

    Todo:
        check what unit the frequencies in
        check why voltage are 0

    """
    logger.debug(f"cavity property {prop=}")
    p = Cavity(**prop)
    voltage = p.cavity_configuration.voltage

    energy = energy
    return at.RFCavity(
        p.name,
        length=p.length,
        frequency=p.cavity_configuration.frequency,
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
    Sextupole=instanitate_sextupole,
    Corrector=instanitate_steerer,
    Octupole=instanitate_octupole,
)

# due to historic reasons: need to get the that cleaned away
factory_dict_default["Monitor"] = factory_dict_default["Monitor"]
