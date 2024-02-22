"""build sequence of accelerator toolbox lattice elements
"""
import enum
import math
from functools import partial

import at
import jsons

from ...model.element import Element

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
    p = jsons.load(prop, Element)
    return factory_dict[p.type](p)


def instantiate_marker(prop: Element):
    #: Todo re
    return at.Marker(prop.name, length=0)


def instantiate_monitor(prop: Element):
    #: Todo re
    return at.Monitor(prop.name, length=0)


def instantiate_drift(prop: Element):
    return at.Drift(prop.name, length=prop.length)


def instantiate_bending(prop: Element):
    """


    Todo:
        reference to definition
        Check in which units angles are stored in lat2d
        Check in which units angles are used by at

        Check what the definition of h is
    """
    h = 0.0

    #: Todo: should irho be checked then
    return at.Dipole(
        prop.name,
        h=h,
        ExitAngle=prop.exitangle,
        EntranceAngle=prop.entranceangle,
        bending_angle=prop.bendingangle,
        k=0.0,
        length=prop.length,
    )


def instanitate_quadrupole(prop: Element):
    """
    Todo:
    check which convention k follows
    """
    k = prop.main_multipole_strength
    return at.Quadrupole(prop.name, length=prop.length, k=k)


#


def instanitate_sextupole(prop: Element):
    """
    Todo:
        check which convention h follows?
    """
    h = prop.main_multipole_strength
    return at.Sextupole(prop.name, length=prop.length, h=h)


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


def instaniate_cavity(prop: Element, *, energy):
    """Instanitate a heavily broken element

    Using voltage is inconsistent with using K values for quad
    Energy is a property of the beam not of the cavity

    Todo:
        check what unit the frequencies in
        check why voltage are 0

    """
    voltage = prop.voltage
    voltage = 0
    energy = energy
    return at.RFCavity(
        prop.name,
        length=prop.length,
        frequency=prop.frequency,
        harmonic_number=prop.harmnumber,
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
    Horizontalsteerer=partial(
        instanitate_steerer, orientation=SteererOrientation.horizontal
    ),
    Verticalsteerer=partial(
        instanitate_steerer, orientation=SteererOrientation.horizontal
    ),
)

# due to historic reasons: need to get the that cleaned away
factory_dict_default["HorizontalSteerer"] = factory_dict_default["Horizontalsteerer"]
factory_dict_default["VerticalSteerer"] = factory_dict_default["Verticalsteerer"]
factory_dict_default["Monitor"] = factory_dict_default["Monitor"]
