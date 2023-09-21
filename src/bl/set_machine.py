import copy
import logging

import jsons
from fastapi import FastAPI
from pymongo import MongoClient

from src.controller import machine_controller
from src.model.beam_position_monitor import BeamPositionMonitor
from src.model.bending import Bending
from src.model.cavity import Cavity
from src.model.drift import Drift
from src.model.horizontal_steerer import HorizontalSteerer
from src.model.machine import Machine
from src.model.marker import Marker
from src.model.quadrupole import Quadrupole
from src.model.sequencer import Sequencer
from src.model.sextupole import Sextupole
from src.model.vertical_steerer import VerticalSteerer

#
app = FastAPI()
app.include_router(machine_controller.router, tags=["machines"], prefix="/machine")
# app.mongodb_client = MongoClient("mongodb://mongodb.bessy.de:27017/") use this if you want to write to the besy server
app.mongodb_client = MongoClient("mongodb://localhost:27017/") # use this if you are writing to your local machine.
app.database = app.mongodb_client["bessyii"]

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

        if type_name in ["Bending", "Quadrupole", "Sextupole", "HorizontalSteerer", "VerticalSteerer"]:
            row.setdefault("main_multipole_strength", row.pop("K", 0e0))  # rename "K" to "main_multipole_strength"
            row.setdefault("number_of_integration_steps",
                           row.pop("N", 1))  # rename "N" to "number_of_integration_steps"
            row.setdefault("method", row.pop("Method", 4))  # rename "Method" to "method"
        elif type_name == "Cavity":
            row.setdefault("frequency", row.pop("Frequency", 0e0))  # rename "Frequency" to "frequency"
            row.setdefault("voltage", row.pop("Voltage", 0e0))  # rename "Voltage" to "voltage"
            row.setdefault("harmonic_number",
                           row.pop("HarmonicNumber", 0e0))  # rename "HarmonicNumber" to "harmonic_number"
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
            "Bending": (Bending, machine.add_bending),
            "Quadrupole": (Quadrupole, machine.add_quadrupole),
            "BPM": (BeamPositionMonitor, machine.add_beam_position_monitor),
            "VerticalSteerer": (VerticalSteerer, machine.add_vertical_steerer),
            "HorizontalSteerer": (HorizontalSteerer, machine.add_horizontal_steerer),
            "Cavity": (Cavity, machine.add_cavity),
        }

        type_class, type_method = type_dict.get(type_name, (None, None))
        if type_class is None or type_method is None:
            raise KeyError(f"Don't know type {type_name}")
        sequence_item.set_properties(row)
        type_instance = type_class(**row)
        machine.add_to_sequence(sequence_item)
        type_method(type_instance)

    # return machine
    from starlette.testclient import TestClient
    with TestClient(app) as client:
        response = client.post("/machine/", json=jsons.dump(machine))
        if response.status_code != 201:
            raise AssertionError(f"Got response {response}")
