import os

import jsons
from starlette.testclient import TestClient

from fastapi import FastAPI
from pymongo import MongoClient

from .. import mongodb_url
from ..model.machine import Machine
from ..controller import machine_controller


app = FastAPI()
app.include_router(machine_controller.router, tags=["machines"], prefix="/machine")
app.mongodb_client = MongoClient(mongodb_url)
DB_NAME = os.environ.get("MONGODB_DB", "bessyii")
app.database = app.mongodb_client[DB_NAME]

def set_machine(machine: Machine):
# return machine

    with TestClient(app) as client:
        response = client.post("/machine/machine", json=jsons.dump(machine.to_dict()))
        if response.status_code != 201:
            raise AssertionError(f"Got response {response}")

