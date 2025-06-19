import logging
import os
import datetime
import pprint
from typing import Dict

import jsons
from fastapi import FastAPI
from numpy.random import geometric
from pymongo import MongoClient

from lat2db import mongodb_url
from lat2db.controller import machine_controller
from lat2db.model.beam_position_monitor import BeamPositionMonitor
from lat2db.model.bending import Bending
from lat2db.model.cavity import Cavity
from lat2db.model.drift import Drift
from lat2db.model.geometric_info import GeometricInfo
from lat2db.model.machine import Machine, extract_physics_info_from_lattice, extact_version_from_lattice
from lat2db.model.marker import Marker
from lat2db.model.physics_info import PhysicsInfo
from lat2db.model.quadrupole import Quadrupole
from lat2db.model.sextupole import Sextupole
from lat2db.model.steerer import Steerer
from lat2db.model.version import Version

app = FastAPI()
app.include_router(machine_controller.router, tags=["machines"], prefix="/machine")
app.mongodb_client = MongoClient(mongodb_url)
DB_NAME = os.environ.get("MONGODB_DB", "bessyii")
app.database = app.mongodb_client[DB_NAME]

logger = logging.getLogger("tools")



type_dict_default = {
    "Drift": (Drift),
    "Marker": (Marker),
    "Sextupole": (Sextupole),
    "Steerer": (Steerer),
    "Bending": (Bending),
    "Quadrupole": (Quadrupole),
    "Bpm": (BeamPositionMonitor),
    "Cavity": (Cavity),
    "Horizontalsteerer": None,
    "Verticalsteerer": None,
}


def create_machine(lat, type_dict=type_dict_default):

    elms = [process_element(standardise_element_info(row_), type_dict=type_dict) for row_ in lat.elements]
    # Todo: how to hande elements we are not processing further ...
    # shall one add a place holder
    elms = [elm for elm in elms if elm is not None]
    machine = Machine(
        sequences=[elms],
        version=extact_version_from_lattice(lat.lattice_standard_metadata.lattice_version),
        phyics_info=extract_physics_info_from_lattice(lat.properties.physics.energy),
        geometric_info=GeometricInfo(is_ring=lat.properties.geometric.is_ring),
        name=lat.lattice_standard_metadata.machine_name,
        closed=lat.lattice_standard_metadata.closed
    )


    pprint.pprint(machine)
    return

    # machine.set_base_parameters( lat )


    # machine.add_to_sequence(elms)
    # type_method(type_instance)

    # return machine
    from starlette.testclient import TestClient
    with TestClient(app) as client:
        response = client.post("/machine/machine", json=jsons.dump(machine))
        if response.status_code != 201:
            raise AssertionError(f"Got response {response}")


def process_element(elem_info: Dict, *, type_dict):
    type_class = type_dict[elem_info['type']]
    if not type_class:
        return None
    return type_class(**elem_info)


def standardise_element_info(elem_info: Dict, *, copy: bool = True):
    # iterate through each row in lat.elements

    # make a copy of the row so that changes don't affect original data
    if copy:
        elem_info = elem_info.copy()

    # print the row
    logger.debug('elem_info= %s', elem_info)

    # revamp parameters as required for the dataclasses
    elem_info.setdefault("length", elem_info.pop("L", 0e0))  # rename "L" to "length"
    type_name = elem_info['type']
    # Ensure 'passmethod' and 'tags' keys exist in the row dictionary
    elem_info.setdefault("passmethod", None)
    elem_info.setdefault("tags", None)
    if type_name in ["Bending", "Quadrupole", "Sextupole", "Steerer"]:
        elem_info.setdefault("main_multipole_strength", elem_info.pop("K", 0e0))  # rename "K" to "main_multipole_strength"
        elem_info.setdefault("number_of_integration_steps",
                       elem_info.pop("N", 1))  # rename "N" to "number_of_integration_steps"
        elem_info.setdefault("method", elem_info.pop("Method", 4))  # rename "Method" to "method"
    elif type_name == "Cavity":
        elem_info.setdefault("frequency", elem_info.pop("Frequency", 0e0))  # rename "Frequency" to "frequency"
        elem_info.setdefault("voltage", elem_info.pop("Voltage", 0e0))  # rename "Voltage" to "voltage"
        elem_info.setdefault("harmonic_number",
                       elem_info.pop("Harmonicnumber", 0e0))  # rename "HarmonicNumber" to "harmonic_number"
    else:
        pass  # do nothing if type_name is not recognized

    if type_name == "Bending":
        elem_info.setdefault("bending_angle", elem_info.pop("T", 0e0))  # rename "T" to "bending_angle"
        elem_info.setdefault("entry_angle", elem_info.pop("T1", 0e0))  # rename "T1" to "entry_angle"
        elem_info.setdefault("exit_angle", elem_info.pop("T2", 0e0))  # rename "T2" to "exit_angle"


    return elem_info
