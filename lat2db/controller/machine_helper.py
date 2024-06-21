from dataclasses import asdict,is_dataclass
from typing import List, Dict,Union

from  uuid import uuid4
from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from lat2db.controller.get_machine_output import get_machine_as_json_from_db
from lat2db.model.machine import Machine, Quadrupole, Sextupole, Drift, Marker, BeamPositionMonitor
from lat2db.model.update_machine import MachineUpdate
from pydantic import BaseModel
from pymongo.collection import Collection
from copy import deepcopy
from datetime import datetime


class Quadrupole_request_update(BaseModel):
    affected_drift: str
    updated_data: Quadrupole

### Quad & Sext section

class MagnetUpdateRequest(BaseModel):
    affected_drift: str
    updated_data: Union[Quadrupole, Sextupole]

def update_magnet_details(id: str, magnet_name: str, request_body: MagnetUpdateRequest, magnet_type: str, request: Request):
    database: Collection = request.app.database["machines"]
    machine = database.find_one({"id": str(id)})
    if machine:
        if magnet_type in machine:
            magnet_list = machine.get(magnet_type, [])
            operations = None
            difference = 0
            for magnet_index, magnet in enumerate(magnet_list):
                if magnet.get("name") == request_body.updated_data.name:
                    magnet_length = magnet.get("length")
                    if float(magnet_length) > float(request_body.updated_data.length):
                        operations = "+"
                        difference = float(magnet_length) - float(request_body.updated_data.length)
                    else:
                        operations = "-"
                        difference = float(request_body.updated_data.length) - float(magnet_length)

                    magnet_list.pop(magnet_index)

                    if is_dataclass(request_body.updated_data):
                        update_data_dict = asdict(request_body.updated_data)
                    else:
                        update_data_dict = request_body.updated_data.dict()

                    magnet_list.insert(magnet_index, update_data_dict)
                    break

            database.update_one({"id": str(id)}, {"$set": {magnet_type: magnet_list}})
            affected_drift = request_body.affected_drift
            # update sequence
            if "sequences" in machine:
                sequences_list = machine.get("sequences", [])
                for item_index, item in enumerate(sequences_list):
                    if item.get("name") == request_body.updated_data.name and item.get("type") == magnet_type:
                        sequences_list.pop(item_index)
                        sequences_list.insert(item_index, update_data_dict)
                        break
                if affected_drift != "-1":
                    for item_index, item in enumerate(sequences_list):
                        if int(item.get("index")) == int(affected_drift):
                            if operations == "+":
                                item["length"] = float(item.get("length")) + difference
                            else:
                                item["length"] = float(item.get("length")) - difference
                            sequences_list[item_index] = item
                            break

            database.update_one({"id": str(id)}, {"$set": {"sequences": sequences_list}})
            # update drift
            if "drifts" in machine and affected_drift != "-1":
                drift_list = machine.get("drifts", [])
                for drift_index, drift in enumerate(drift_list):
                    if int(drift.get("index")) == int(affected_drift):
                        if operations == "+":
                            drift["length"] = float(drift.get("length")) + difference
                        else:
                            drift["length"] = float(drift.get("length")) - difference
                        break
                database.update_one({"id": str(id)}, {"$set": {"drifts": drift_list}})

            return JSONResponse(status_code=200, content={"data": machine.get(magnet_type, [])})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


### others Section

class ElementUpdateRequest(BaseModel):
    affected_element: str
    updated_data: Union[Drift, Marker, BeamPositionMonitor]
    
def update_element_details(id: str, element_name: str, element_type: str, request_body: ElementUpdateRequest, request: Request):
    database: Collection = request.app.database["machines"]
    machine = database.find_one({"id": str(id)})
    print("element_name",element_name)
    print("request_body",request_body)
    print("type",element_type)
    if machine:
        if element_type in machine:
            element_list = machine.get(element_type, [])
            operations = None
            difference = 0

            for element_index, element in enumerate(element_list):
                if element.get("name") == element_name:
                    element_length = element.get("length")
                    if float(element_length) > float(request_body.updated_data.length):
                        operations = "+"
                        difference = float(element_length) - float(request_body.updated_data.length)
                    else:
                        operations = "-"
                        difference = float(request_body.updated_data.length) - float(element_length)

                    element_list[element_index] = asdict(request_body.updated_data)

                    database.update_one({"id": str(id)}, {"$set": {element_type: element_list}})

                    if request_body.affected_element != "-1":
                        if "sequences" in machine:
                            sequences_list = machine.get("sequences", [])
                            for item_index, item in enumerate(sequences_list):
                                if item.get("name") == element_name and item.get("type") == element_type.capitalize():
                                    item["length"] = float(item.get("length")) + difference if operations == "+" else float(item.get("length")) - difference
                                    sequences_list[item_index] = item
                                    break
                            database.update_one({"id": str(id)}, {"$set": {"sequences": sequences_list}})

                    return JSONResponse(status_code=200, content={"message": f"{element_type} updated"})

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{element_type.capitalize()} '{element_name}' not found in machine with ID {id}")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")





