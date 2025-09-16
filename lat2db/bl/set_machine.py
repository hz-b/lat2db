import copy
import logging
import os

import jsons
from fastapi import FastAPI
from pymongo import MongoClient

from lat2db import mongodb_url
from lat2db.controller import machine_controller
from lat2db.model.beam_position_monitor import BeamPositionMonitor
from lat2db.model.bending import Bending
from lat2db.model.cavity import Cavity
from lat2db.model.drift import Drift
from lat2db.model.machine import Machine
from lat2db.model.marker import Marker
from lat2db.model.octupole import Octupole
from lat2db.model.quadrupole import Quadrupole
from lat2db.model.sequencer import Sequencer
from lat2db.model.sextupole import Sextupole
from lat2db.model.steerer import Steerer

app = FastAPI()
app.include_router(machine_controller.router, tags=["machines"], prefix="/machine")
app.mongodb_client = MongoClient(mongodb_url)
DB_NAME = os.environ.get("MONGODB_DB", "bessyii")
app.database = app.mongodb_client[DB_NAME]

logger = logging.getLogger("tools")


def create_machine(lat):
    machine = Machine()
    machine.set_base_parameters( lat )

    # iterate through each row in lat.elements
    for row_ in lat.elements:

        # make a copy of the row so that changes don't affect original data
        row = copy.copy(row_)

        # print the row
        print(f'{row} ----')

        # revamp parameters as required for the dataclasses
        row.setdefault("length", row.pop("L", 0e0))  # rename "L" to "length"
        type_name = row['type']
        # Ensure 'passmethod' and 'tags' keys exist in the row dictionary
        row.setdefault("passmethod", None)
        row.setdefault("tags", None)
        if type_name in ["Bending", "Quadrupole", "Sextupole", "Octupole", "Steerer"]:
            row.setdefault("main_multipole_strength", row.pop("K", 0e0))  # rename "K" to "main_multipole_strength"
            row.setdefault("number_of_integration_steps",
                           row.pop("N", 1))  # rename "N" to "number_of_integration_steps"
            row.setdefault("method", row.pop("Method", 4))  # rename "Method" to "method"
        elif type_name == "Cavity":
            row.setdefault("frequency", row.pop("Frequency", 0e0))  # rename "Frequency" to "frequency"
            row.setdefault("voltage", row.pop("Voltage", 0e0))  # rename "Voltage" to "voltage"
            row.setdefault("harmonic_number",
                           row.pop("Harmonicnumber", 0e0))  # rename "HarmonicNumber" to "harmonic_number"
        else:
            pass  # do nothing if type_name is not recognized

        if type_name == "Bending":
            row.setdefault("bending_angle", row.pop("T", 0e0))  # rename "T" to "bending_angle"
            row.setdefault("entry_angle", row.pop("T1", 0e0))  # rename "T1" to "entry_angle"
            row.setdefault("exit_angle", row.pop("T2", 0e0))  # rename "T2" to "exit_angle"

        # create a Sequencer instance using the modified row
        sequence_item = Sequencer(**row)

        # add the sequence_item to the appropriate list in the machine instance based on its type_name
        type_dict = {
            "Drift": (Drift, machine.add_drift),
            "Marker": (Marker, machine.add_marker),
            "Sextupole": (Sextupole, machine.add_sextupole),
            "Octupole": (Octupole, machine.add_octupole),
            "Steerer": (Steerer, machine.add_steerer()),
            "Bending": (Bending, machine.add_bending),
            "Quadrupole": (Quadrupole, machine.add_quadrupole),
            "Bpm": (BeamPositionMonitor, machine.add_beam_position_monitor),
            "Cavity": (Cavity, machine.add_cavity),
        }

        type_class, type_method = type_dict.get(type_name, (None, None))
        if type_class is None or type_method is None:
            if type_name in ['Horizontalsteerer','Verticalsteerer']:
                continue #ignore the two steerers
            else:
                raise KeyError(f"Don't know type {type_name}")
        sequence_item.set_properties(row)
        type_instance = type_class(**row)
        machine.add_to_sequence(sequence_item)
        type_method(type_instance)

    # return machine
    from starlette.testclient import TestClient
    with TestClient(app) as client:
        response = client.post("/machine/machine", json=jsons.dump(machine))
        if response.status_code != 201:
            raise AssertionError(f"Got response {response}")
