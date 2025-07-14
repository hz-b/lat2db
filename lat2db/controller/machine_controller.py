from dataclasses import asdict,is_dataclass
from typing import List, Dict

import uuid
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

router = APIRouter()


@router.get("/test2", response_description="Test machine endpoint")
def test_machine_endpoint():
    return {"message": "Test machine endpoint"}


@router.get("/test4", response_description="Test machine endpoint")
def test_machine_endpoint():
    return {"message": "Test machine endpoint44"}


@router.post("/machine", response_description="Create a new machine", status_code=status.HTTP_201_CREATED,
             response_model=Machine)
def create_machine(request: Request, machine: Machine = Body(...)):
    machine = jsonable_encoder(machine)
    new_machine = request.app.database["machines"].insert_one(machine)
    created_machine = request.app.database["machines"].find_one(
        {"_id": new_machine.inserted_id}
    )
    return created_machine


@router.get("/machine", response_description="List all Machines", response_model=List[Machine])
def list_machines(request: Request):
    machines = list(request.app.database["machines"].find(limit=100))
    return machines


@router.get("/machine/{id}", response_description="Get a single machine by id", response_model=Machine)
def find_a_machine(id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine
    if (machine := request.app.database["machines"].find_one({"_id": ObjectId(id)})) is not None:
        return machine
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


# get all Quads
@router.get("/machine/{id}/quad", response_description="Get machine quads by id", response_model=List[Quadrupole])
def find_quads(id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["quadrupoles"]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


def filter_quads(tags: List[str], quads: List[Quadrupole]) -> Dict[str, List[Dict]]:
    result = {}
    for quad in quads:
        if any(tag in quad.get('tags', []) for tag in tags):
            result.setdefault("quadrupole", []).append(quad)
    return result


# todo: make it generic so that any field name is provided on the filter and it should return result
# todo: create other device filters such as sextupole dipole and steerer filters
@router.get("/machine/{id}/quad/filter/")
async def filter_quads_by_tags(id: str, request: Request, tags: List[str] = Query(..., min_length=1)) -> JSONResponse:
    if (machine := request.app.database["machines"].find_one({"_id": ObjectId(id)})) is not None:
        return filter_quads(tags, machine["quadrupoles"])


@router.put("/machine/{id}", response_description="Update a machine", response_model=Machine)
def update_machine(id: str, request: Request, machine: MachineUpdate = Body(...)):
    machine_dict = machine.dict(exclude_unset=True)

    if len(machine_dict) >= 1:
        update_result = request.app.database["machines"].update_one(
            {"_id": ObjectId(id)}, {"$set": machine_dict}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")

    # Retrieve the updated machine
    updated_machine = request.app.database["machines"].find_one({"_id": ObjectId(id)})

    if updated_machine:
        return updated_machine

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


@router.delete("/machine/{id}", response_description="Delete a machine")
def delete_machine(id: str, request: Request, response: Response):
    delete_result = request.app.database["machines"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


# update Quadrupoles

class Quadrupole_request_update(BaseModel):
    affected_drift: str
    updated_data: Quadrupole


@router.put("/machine/{id}/quad/{quad_name}", response_description="Update a quadrupole's details")
def update_quadrupole_details(id: str, quad_name: str, request_body: Quadrupole_request_update, request: Request):
    database: Collection = request.app.database["machines"]
    print("pass id is  ", id)
    machine = database.find_one({"id": str(id)})
    update_data_dict = request_body.updated_data
    if is_dataclass(request_body.updated_data):
        update_data_dict = asdict(request_body.updated_data)
    else:
        update_data_dict = request_body.updated_data.dict()
    print("machien is ", machine)
    if machine:
        print("Found machine with ID:", id)
        if "quadrupoles" in machine:
            print("Quadrupoles field exists in the machine document")
            if "quadrupoles" in machine:
                quadrupoles_list = machine.get("quadrupoles", [])
                sequences_list = machine.get("sequences", [])
                operations = None
                difference = 0
                print("######passed index is ", request_body.updated_data.index)
                for quad_index, quad in enumerate(quadrupoles_list):
                    print("quad indexis ", quad_index)
                    if quad.get("name") == request_body.updated_data.name:
                        quad_length = quad.get("length")
                        if float(quad_length) > float(request_body.updated_data.length):
                            operations = "+"
                            difference = float(quad_length) - float(request_body.updated_data.length)
                        else:
                            operations = "-"
                            difference = float(request_body.updated_data.length) - float(quad_length)

                        removed_quadrupole = quadrupoles_list.pop(quad_index)
                       

                        quadrupoles_list.insert(quad_index, update_data_dict)
                        break

                database.update_one({"id": str(id)}, {"$set": {"quadrupoles": quadrupoles_list}})
                affected_drift = request_body.affected_drift
                # update sequence
                if "sequences" in machine:
                    sequences_list = machine.get("sequences", [])
                    for item_index, item in enumerate(sequences_list):
                        if item.get("name") == request_body.updated_data.name and item.get("type") == "Quadrupole":
                            removed_quadrupole = sequences_list.pop(item_index)
                            # affected_drift=item.get("index")
                            print("******* affected drif index is ", affected_drift)
                            sequences_list.insert(item_index, update_data_dict)
                            break
                    if affected_drift != "-1":
                        for item_index, item in enumerate(sequences_list):
                            if int(item.get("index")) == int(affected_drift):
                                if operations == "+":
                                    item["length"] = float(item.get("length")) + difference
                                    print("drift length is in seq seq ", item["length"])

                                else:
                                    item["length"] = float(item.get("length")) - difference
                                    print("drift length is in seq seq ", item["length"])

                                sequences_list[item_index] = item
                                print("**** drift in the sequence is updated")
                                # sequences_list.insert(item_index, asdict(request_body.updated_data))
                                break

                database.update_one({"id": str(id)}, {"$set": {"sequences": sequences_list}})
                # update drift
                print("affected dfridt is ",affected_drift)
                if "drifts" in machine and affected_drift != "-1":
                    print("drift update is intiated")
                    drift_list = machine.get("drifts", [])
                    for drift_index, drift in enumerate(drift_list):
                        if int(drift.get("index")) == int(affected_drift):
                            if operations == "+":
                                drift["length"] = float(drift.get("length")) + difference
                                print("drift length is in drift seq ", drift["length"])
                            else:
                                drift["length"] = float(drift.get("length")) - difference
                                print("drift length is iin drift seq ", drift["length"])
                            break
                    database.update_one({"id": str(id)}, {"$set": {"drifts": drift_list}})

                    print("**** drift in the drift list is updated")

                return JSONResponse(status_code=200, content={"message": f"Quadrupole updated"})



# update the copy of the quadrupole

@router.put("/machine/{id}/quad_copy/{quad_name}", response_description="Update a quadrupole's details")
def update_quadrupole_details_copy(id: str, quad_name: str, request_body: Quadrupole_request_update, request: Request):
    # you should be able to call your normal quad update after a new record is created
    # e.g: simply call two functions under the new service (duplicateMachine)
    # whenever the duplicate machine service is called from UI then call two functions
    #   1. create new machine
    #       1.1 get existing machine call the service (see get_machine_output.py)
    machine = get_machine_as_json_from_db(id)
    #       1.2 make your changes (change name and assign a new id)

    if machine:
        machine_copy = deepcopy(machine)
        old_name=machine_copy.pop("name")
        current_date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        machine_copy["name"]=f"{old_name}_{current_date_time}"
        new_id = str(uuid.uuid4())
        machine_copy['id'] = new_id
        machine_copy["_id"] = ObjectId()
        database: Collection = request.app.database["machines"]
    #       1.3 insert the updated machine into db
        database.insert_one(machine_copy)
    #   2. update quad (this you already have) just move the functionality under a function
    #     update_quad(machine)
    #   and move that function to a different file called machine_update_helper.
    #   this function should be dynamic so that a quad/sextupole or any other type of element can be updated.
    #   this means you don't write  the code again and again with very little changes.


    database: Collection = request.app.database["machines"]
    print("pass id is  ", id)
    machine = database.find_one({"id": str(id)})
    print("machien is ", machine)
    update_data_dict = request_body.updated_data
    if is_dataclass(request_body.updated_data):
        update_data_dict = asdict(request_body.updated_data)
    else:
        update_data_dict = request_body.updated_data.dict()
    if machine:

        # machine_copy = deepcopy(machine)
        pre_id = machine_copy.pop("id")
        # current_date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # pre_id=f"{pre_id}-{current_date_time}"
        # machine_copy["id"] =pre_id
        # #create id like this: uuid.uuid4 no need to create a similar id to the old one
        # machine_copy["_id"]=ObjectId()   # mongo will add this field no need to forcefully generate it
        # old_name=machine_copy.pop("name")
        # machine_copy["name"]=f"{old_name}_{current_date_time}"
        # database.insert_one(machine_copy)
        if "quadrupoles" in machine_copy:
            # you should be able to call your normal quad update after a new record is created
            # e.g: simply call two functions under the new service (duplicateMachine)
            # whenever the duplicate machine service is called from UI then call two functions
            #   1. create new machine
            #       1.1 get existing machine call the service (see get_machine_output.py)
            #       1.2 make your changes (change name and assign a new id)
            #       1.3 insert the updated machine into db
            #   2. update quad (this you already have) just move the functionality under a function
            #   and move that function to a different file called machine_update_helper.
            #   this function should be dynamic so that a quad/sextupole or any other type of element can be updated.
            #   this means you don't write  the code again and again with very little changes.

            if "quadrupoles" in machine_copy:
                quadrupoles_list = machine_copy.get("quadrupoles", [])
                sequences_list = machine_copy.get("sequences", [])
                operations = None
                difference = 0
                for quad_index, quad in enumerate(quadrupoles_list):
                    print("quad indexis ", quad_index)
                    if quad.get("name") == request_body.updated_data.name:
                        quad_length = quad.get("length")
                        if float(quad_length) > float(request_body.updated_data.length):
                            operations = "+"
                            difference = float(quad_length) - float(request_body.updated_data.length)
                        else:
                            operations = "-"
                            difference = float(request_body.updated_data.length) - float(quad_length)

                        
                        quadrupoles_list.insert(quad_index, update_data_dict)
                        break

                
                database.update_one({"id": str(pre_id)}, {"$set": {"quadrupoles": quadrupoles_list}})
                affected_drift = request_body.affected_drift
                # update sequence
                if "sequences" in machine_copy:
                    sequences_list = machine_copy.get("sequences", [])
                    for item_index, item in enumerate(sequences_list):
                        if item.get("name") == request_body.updated_data.name and item.get("type") == "Quadrupole":
                            removed_quadrupole = sequences_list.pop(item_index)
                            # affected_drift=item.get("index")
                            print("******* affected drif index is ", affected_drift)
                            sequences_list.insert(item_index, update_data_dict)
                            break
                    if affected_drift != "-1":
                        for item_index, item in enumerate(sequences_list):
                            if int(item.get("index")) == int(affected_drift):
                                if operations == "+":
                                    item["length"] = float(item.get("length")) + difference
                                    print("drift length is in seq seq ", item["length"])

                                else:
                                    item["length"] = float(item.get("length")) - difference
                                    print("drift length is in seq seq ", item["length"])

                                sequences_list[item_index] = item
                                print("**** drift in the sequence is updated")
                                # sequences_list.insert(item_index, asdict(request_body.updated_data))
                                break

                database.update_one({"id": str(pre_id)}, {"$set": {"sequences": sequences_list}})
                # update drift
                print("affected dfridt is ",affected_drift)
                if "drifts" in machine_copy and affected_drift != "-1":
                    print("drift update is intiated")
                    drift_list = machine_copy.get("drifts", [])
                    for drift_index, drift in enumerate(drift_list):
                        if int(drift.get("index")) == int(affected_drift):
                            if operations == "+":
                                drift["length"] = float(drift.get("length")) + difference
                                print("drift length is in drift seq ", drift["length"])
                            else:
                                drift["length"] = float(drift.get("length")) - difference
                                print("drift length is iin drift seq ", drift["length"])
                            break
                    database.update_one({"id": str(pre_id)}, {"$set": {"drifts": drift_list}})

                    print("**** drift in the drift list is updated")

                return JSONResponse(status_code=200, content={"message": f"Quadrupole updated"})


# get all Sextupoles

@router.get("/machine/{id}/sextupole", response_description="Get a single machine by id",
            response_model=List[Sextupole])
def find_a_machine(id: str, request: Request):
    print("inside the quad get function")
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["sextupoles"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


# update Sextuploles

class Sextupole_request_update(BaseModel):
    affected_drift: str
    updated_data: Sextupole


@router.put("/machine/{id}/sext/{sext_name}", response_description="Update a sextupole's details")
def update_sextupole_details(id: str, sext_name: str, request_body: Sextupole_request_update, request: Request):
    print("Inside the update function ")
    database: Collection = request.app.database["machines"]
    print("pass id is  ", id)
    machine = database.find_one({"id": str(id)})
    update_data_dict = request_body.updated_data
    if is_dataclass(request_body.updated_data):
        update_data_dict = asdict(request_body.updated_data)
    else:
        update_data_dict = request_body.updated_data.dict()
    print("machien is ", machine)
    if machine:
        print("Found machine with ID:", id)
        if "sextupoles" in machine:
            print("sextupoles field exists in the machine document")
            if "sextupoles" in machine:
                sextupole_list = machine.get("sextupoles", [])
                operations = None
                difference = 0

                print("######passed index is ", request_body.updated_data.index)
                for sext_index, sext in enumerate(sextupole_list):
                    print("sext indexis ", sext_index)
                    if sext.get("name") == request_body.updated_data.name:
                        sext_length = sext.get("length")
                        if float(sext_length) > float(request_body.updated_data.length):
                            operations = "+"
                            difference = float(sext_length) - float(request_body.updated_data.length)
                        else:
                            operations = "-"
                            difference = float(request_body.updated_data.length) - float(sext_length)

                        removed_sextupoles = sextupole_list.pop(sext_index)
                      

                        sextupole_list.insert(sext_index, update_data_dict)
                        print("inserted.")
                        break

                database.update_one({"id": str(id)}, {"$set": {"sextupoles": sextupole_list}})
                affected_drift = request_body.affected_drift
                # update sequence
                if "sequences" in machine:
                    sequences_list = machine.get("sequences", [])
                    for item_index, item in enumerate(sequences_list):
                        if item.get("name") == request_body.updated_data.name and item.get("type") == "Sextupole":
                            removed_sextupole = sequences_list.pop(item_index)
                            sequences_list.insert(item_index, update_data_dict)
                            break
                    if affected_drift != "-1":
                        for item_index, item in enumerate(sequences_list):
                            if int(item.get("index")) == int(affected_drift):
                                if operations == "+":
                                    item["length"] = float(item.get("length")) + difference
                                    print("drift length is in seq seq ", item["length"])

                                else:
                                    item["length"] = float(item.get("length")) - difference
                                    print("drift length is in seq seq ", item["length"])

                                sequences_list[item_index] = item
                                print("**** drift in the sequence is updated")
                                # sequences_list.insert(item_index, asdict(request_body.updated_data))
                                break

                database.update_one({"id": str(id)}, {"$set": {"sequences": sequences_list}})
                # update drift
                if "drifts" in machine and affected_drift != "-1":
                    drift_list = machine.get("drifts", [])
                    for drift_index, drift in enumerate(drift_list):
                        if int(drift.get("index")) == int(affected_drift):
                            if operations == "+":
                                drift["length"] = float(drift.get("length")) + difference
                                print("drift length is in drift seq ", drift["length"])
                            else:
                                drift["length"] = float(drift.get("length")) - difference
                                print("drift length is iin drift seq ", drift["length"])
                            break
                    database.update_one({"id": str(id)}, {"$set": {"drifts": drift_list}})
                    print("**** drift in the drift list is updated")

                return JSONResponse(status_code=200, content={"message": f"Sextupoles updated"})


# update sextupole copy

@router.put("/machine/{id}/sext_copy/{sext_name}", response_description="Update a sextupole's details")
def update_sextupole_details_copy(id: str, sext_name: str, request_body: Sextupole_request_update, request: Request):
    
    database: Collection = request.app.database["machines"]
    print("pass id is  ", id)
    machine = database.find_one({"id": str(id)})
    print("machien is ", machine)
    update_data_dict = request_body.updated_data
    if is_dataclass(request_body.updated_data):
        update_data_dict = asdict(request_body.updated_data)
    else:
        update_data_dict = request_body.updated_data.dict()
    if machine:
        machine_copy = deepcopy(machine)
        pre_id = machine_copy.pop("id")
        current_date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        pre_id=f"{pre_id}-{current_date_time}"
        machine_copy["id"] =pre_id
        machine_copy["_id"]=ObjectId()
        old_name=machine_copy.pop("name")
        machine_copy["name"]=f"{old_name}_{current_date_time}"
        database.insert_one(machine_copy)
        if "sextupoles" in machine_copy:
            print("sextupoles field exists in the machine document")
            if "sextupoles" in machine_copy:
                sextupole_list = machine_copy.get("sextupoles", [])
                operations = None
                difference = 0
                print("######passed index is ", request_body.updated_data.index)
                for sext_index, sext in enumerate(sextupole_list):
                    print("sext indexis ", sext_index)
                    if sext.get("name") == request_body.updated_data.name:
                        sext_length = sext.get("length")
                        if float(sext_length) > float(request_body.updated_data.length):
                            operations = "+"
                            difference = float(sext_length) - float(request_body.updated_data.length)
                        else:
                            operations = "-"
                            difference = float(request_body.updated_data.length) - float(sext_length)

                        removed_sextupoles = sextupole_list.pop(sext_index)
                        

                        sextupole_list.insert(sext_index, update_data_dict)
                        print("inserted.")
                        break

                database.update_one({"id": str(pre_id)}, {"$set": {"sextupoles": sextupole_list}})
                affected_drift = request_body.affected_drift
                # update sequence
                if "sequences" in machine_copy:
                    sequences_list = machine_copy.get("sequences", [])
                    for item_index, item in enumerate(sequences_list):
                        if item.get("name") == request_body.updated_data.name and item.get("type") == "Sextupole":
                            removed_sextupole = sequences_list.pop(item_index)
                            sequences_list.insert(item_index, update_data_dict)
                            break
                    if affected_drift != "-1":
                        for item_index, item in enumerate(sequences_list):
                            if int(item.get("index")) == int(affected_drift):
                                if operations == "+":
                                    item["length"] = float(item.get("length")) + difference
                                    print("drift length is in seq seq ", item["length"])

                                else:
                                    item["length"] = float(item.get("length")) - difference
                                    print("drift length is in seq seq ", item["length"])

                                sequences_list[item_index] = item
                                print("**** drift in the sequence is updated")
                                # sequences_list.insert(item_index, asdict(request_body.updated_data))
                                break

                database.update_one({"id": str(pre_id)}, {"$set": {"sequences": sequences_list}})
                # update drift
                if "drifts" in machine_copy and affected_drift != "-1":
                    drift_list = machine_copy.get("drifts", [])
                    for drift_index, drift in enumerate(drift_list):
                        if int(drift.get("index")) == int(affected_drift):
                            if operations == "+":
                                drift["length"] = float(drift.get("length")) + difference
                                print("drift length is in drift seq ", drift["length"])
                            else:
                                drift["length"] = float(drift.get("length")) - difference
                                print("drift length is iin drift seq ", drift["length"])
                            break
                    database.update_one({"id": str(pre_id)}, {"$set": {"drifts": drift_list}})
                    print("**** drift in the drift list is updated")

                return JSONResponse(status_code=200, content={"message": f"Sextupoles updated"})


# get all Drifts

@router.get("/machine/{id}/drifts", response_description="Get a single machine by id", response_model=List[Drift])
def find_a_machine(id: str, request: Request):
    print("inside the drif get function")
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["drifts"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


# update Drifts

class Drift_request_update(BaseModel):
    affected_drift: str
    updated_data: Drift


@router.put("/machine/{id}/drift/{drift_name}", response_description="Update a Drift's details")
def update_drift_details(id: str, drift_name: str, request_body: Drift_request_update, request: Request):
    print("Inside the update function ")
    database: Collection = request.app.database["machines"]
    print("pass id is  ", id)
    machine = database.find_one({"id": str(id)})
    print("machien is ", machine)
    if machine:
        print("Found machine with ID:", id)
        if "drifts" in machine:
            print("drifts field exists in the machine document")
            if "drifts" in machine:
                drift_list = machine.get("drifts", [])
                operations = None
                difference = 0
                print("######passed index is ", request_body.updated_data.index)
                for drift_index, drift in enumerate(drift_list):
                    print("drift indexis ", drift_index)
                    if drift.get("name") == request_body.updated_data.name:
                        drift_length = drift.get("length")
                        if float(drift_length) > float(request_body.updated_data.length):
                            operations = "+"
                            difference = float(drift_length) - float(request_body.updated_data.length)
                        else:
                            operations = "-"
                            difference = float(request_body.updated_data.length) - float(drift_length)

                        removed_drift = drift_list.pop(drift_index)
                        update_data_dict = request_body.updated_data

                        drift_list.insert(drift_index, asdict(request_body.updated_data))
                        print("inserted.")
                        break

                database.update_one({"id": str(id)}, {"$set": {"drifts": drift_list}})
                """ if request_body.affected_drift!="-1":
                    for drift_index, drift in enumerate(drift_list):
                        if int(drift.get("index")) == int(request_body.affected_drift):
                            if operations == "+":
                                drift["length"] = float(drift.get("length")) + difference
                            else:
                                drift["length"] = float(drift.get("length")) - difference

                    database.update_one({"id": str( id)}, {"$set": {"drifts": drift_list}}) """
                if "sequences" in machine:
                    sequences_list = machine.get("sequences", [])
                    for item_index, item in enumerate(sequences_list):
                        if item.get("name") == request_body.updated_data.name and item.get("type") == "Drift":
                            removed_Drift = sequences_list.pop(item_index)
                            sequences_list.insert(item_index, asdict(request_body.updated_data))
                            break
                    database.update_one({"id": str(id)}, {"$set": {"sequences": sequences_list}})

                return JSONResponse(status_code=200, content={"message": f"drifts updated"})


# get all Markers

@router.get("/machine/{id}/markers", response_description="Get a single machine by id", response_model=List[Marker])
def find_a_machine(id: str, request: Request):
    print("inside the drift get function")
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["markers"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


# update Markers

class Marker_request_update(BaseModel):
    affected_marker: str
    updated_data: Marker


@router.put("/machine/{id}/marker/{marker_name}", response_description="Update a markers's details")
def update_drift_details(id: str, marker_name: str, request_body: Marker_request_update, request: Request):
    print("Inside the update function ")
    database: Collection = request.app.database["machines"]
    print("pass id is  ", id)
    machine = database.find_one({"id": str(id)})
    print("machien is ", machine)
    if machine:
        print("Found machine with ID:", id)
        if "markers" in machine:
            print("markers field exists in the machine document")
            if "markers" in machine:
                marker_list = machine.get("markers", [])
                operations = None
                difference = 0
                print("######passed index is ", request_body.updated_data.index)
                for marker_index, marker in enumerate(marker_list):
                    print("marker indexis ", marker_index)
                    if marker.get("name") == request_body.updated_data.name:
                        marker_length = marker.get("length")
                        if float(marker_length) > float(request_body.updated_data.length):
                            operations = "+"
                            difference = float(marker_length) - float(request_body.updated_data.length)
                        else:
                            operations = "-"
                            difference = float(request_body.updated_data.length) - float(marker_length)

                        removed_marker = marker_list.pop(marker_index)
                        update_data_dict = request_body.updated_data
                        print("&&&&&&&& removed ", removed_marker)
                        print("Type of update_data_dict:", type(request_body.updated_data))
                        print("Attributes of update_data_dict:", dir(request_body.updated_data))

                        print("^^^^^^^^^^^^ json converted", asdict(request_body.updated_data))
                        marker_list.insert(marker_index, asdict(request_body.updated_data))
                        print("inserted.")
                        break

                database.update_one({"id": str(id)}, {"$set": {"markers": marker_list}})
                """ if request_body.affected_marker!="-1":
                    for marker_index, marker in enumerate(marker_list):
                        if int(marker.get("index")) == int(request_body.affected_marker):
                            if operations == "+":
                                marker["length"] = float(marker.get("length")) + difference
                            else:
                                marker["length"] = float(marker.get("length")) - difference

                    database.update_one({"id": str( id)}, {"$set": {"markers": marker_list}}) """
                if "sequences" in machine:
                    sequences_list = machine.get("sequences", [])
                    for item_index, item in enumerate(sequences_list):
                        if item.get("name") == request_body.updated_data.name and item.get("type") == "Marker":
                            removed_Marker = sequences_list.pop(item_index)
                            sequences_list.insert(item_index, asdict(request_body.updated_data))
                            break
                    database.update_one({"id": str(id)}, {"$set": {"sequences": sequences_list}})

                return JSONResponse(status_code=200, content={"message": f"markers updated"})


# get all Monitors

@router.get("/machine/{id}/monitors", response_description="Get a single machine by id",
            response_model=List[BeamPositionMonitor])
def find_a_machine(id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["beam_position_monitors"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


# update Monitors

class Monitor_request_update(BaseModel):
    affected_monitor: str
    updated_data: BeamPositionMonitor


@router.put("/machine/{id}/monitor/{monitor_name}", response_description="Update a monitor's details")
def update_monitor_details(id: str, monitor_name: str, request_body: Monitor_request_update, request: Request):
    print("Inside the update function ")
    database: Collection = request.app.database["machines"]
    print("pass id is  ", id)
    machine = database.find_one({"id": str(id)})
    print("machien is ", machine)
    if machine:
        print("Found machine with ID:", id)
        if "beam_position_monitors" in machine:
            print("markers field exists in the machine document")
            if "beam_position_monitors" in machine:
                monitor_list = machine.get("beam_position_monitors", [])
                operations = None
                difference = 0
                print("######passed index is ", request_body.updated_data.index)
                for monitor_index, monitor in enumerate(monitor_list):
                    print("monitor indexis ", monitor_index)
                    if monitor.get("name") == request_body.updated_data.name:
                        monitor_length = monitor.get("length")
                        if float(monitor_length) > float(request_body.updated_data.length):
                            operations = "+"
                            difference = float(monitor_length) - float(request_body.updated_data.length)
                        else:
                            operations = "-"
                            difference = float(request_body.updated_data.length) - float(monitor_length)

                        removed_monitor = monitor_list.pop(monitor_index)
                        update_data_dict = request_body.updated_data
                        print("&&&&&&&& removed ", removed_monitor)
                        print("Type of update_data_dict:", type(request_body.updated_data))
                        print("Attributes of update_data_dict:", dir(request_body.updated_data))

                        print("^^^^^^^^^^^^ json converted", asdict(request_body.updated_data))
                        monitor_list.insert(monitor_index, asdict(request_body.updated_data))
                        print("inserted.")
                        break

                database.update_one({"id": str(id)}, {"$set": {"beam_position_monitors": monitor_list}})
                """ if request_body.affected_monitor!="-1":
                    for monitor_index, monitor in enumerate(monitor_list):
                        if int(monitor.get("index")) == int(request_body.affected_monitor):
                            if operations == "+":
                                monitor["length"] = float(monitor.get("length")) + difference
                            else:
                                monitor["length"] = float(monitor.get("length")) - difference

                    database.update_one({"id": str( id)}, {"$set": {"beam_position_monitors": monitor_list}}) """

                if "sequences" in machine:
                    sequences_list = machine.get("sequences", [])
                    for item_index, item in enumerate(sequences_list):
                        if item.get("name") == request_body.updated_data.name and item.get("type") == "Monitor":
                            removed_Monitor = sequences_list.pop(item_index)
                            sequences_list.insert(item_index, asdict(request_body.updated_data))
                            break
                    database.update_one({"id": str(id)}, {"$set": {"sequences": sequences_list}})
                return JSONResponse(status_code=200, content={"message": f"monitor updated"})


# get the relevenet quad detail from sequence lsit
@router.get("/machine/{id}/get_quad_from_seq/{quad_name}", response_description="listing the quad from sequence")
def get_quadrupole_details_from_sequence(id: str, quad_name: str, request: Request):
    print("Inside the update function ")

    database: Collection = request.app.database[
        "machines"]  # Assuming sequence is a record in the "machines" collection

    machine = database.find_one({"id": str(id)})  # Find the machine record by ID

    if machine:
        print("Found machine with ID:", id)
        sequences = machine.get("sequences", [])
        for sequence in sequences:

            if sequence["name"] == quad_name:  # Assuming sequence name is the same as the quadrupole name

                print("Sequence found with name:", quad_name)
                return sequence

    raise HTTPException(status_code=404,
                        detail=f"Quadrupole with name {quad_name} not found in the sequence collection")


@router.put("/machine/{id}/update_quad_from_seq/{quad_name}", response_description="Update a quadrupole from sequence")
def update_quadrupole_from_sequence(id: str, target_drift: str, quad_name: str, update_data: dict, request: Request):
    print("Inside the update function ")
    database: Collection = request.app.database["machines"]

    machine = database.find_one({"id": str(id)})  # Find the machine id
    if machine:
        print("Found machine with ID:", id)
        sequences = machine.get("sequences", [])
        is_sequence_update = False
        is_quad_updated = False
        for sequence in sequences:
            if str(sequence["index"]) == target_drift and sequence["type"] == "Drift":
                print("inside the drift")
                try:
                    get_qud_prev = database.find_one(
                        {"id": str(id), "sequences": {"$elemMatch": {"name": quad_name, "type": "Quadrupole"}}},
                        projection={"sequences.$": 1}
                    )

                    print("--object of qud for the previous value ", get_qud_prev)
                    if get_qud_prev["sequences"][0]["length"] > update_data["length"]:
                        print("target drift", target_drift)
                        drift_value = database.find_one(
                            {"id": str(id),
                             "sequences": {"$elemMatch": {"index": int(target_drift), "type": "Drift"}}},
                            projection={"sequences.$": 1}
                        )
                        drift_object = drift_value["sequences"][0]

                        prev_value_drift_length = drift_object.get("length", "Length not found")
                        print("----prev drift va", prev_value_drift_length)
                        print("------prev of quad is ", get_qud_prev["sequences"][0]["length"])
                        print("----new valu of qud is ", update_data["length"])
                        update_drift_value = prev_value_drift_length + (
                                get_qud_prev["sequences"][0].get("length", 0) - update_data.get("length", 0))
                        print("updated -------drfit val", update_drift_value)
                        print("updated drift new value is  ", update_drift_value)
                        result = database.update_one(
                            {"id": str(id)},
                            {"$set": {"sequences.$[element].length": update_drift_value}},
                            array_filters=[{"element.index": int(target_drift), "element.type": "Drift"}]
                        )
                        print("updated--------")

                    else:
                        drift_value = database.find_one(
                            {"id": str(id),
                             "sequences": {"$elemMatch": {"index": int(target_drift), "type": "Drift"}}},
                            projection={"sequences.$": 1}
                        )

                        drift_object = drift_value["sequences"][0]
                        prev_value_drift_length = drift_object.get("length", "Length not found")
                        print("prev value of dirf------", prev_value_drift_length)
                        print("new value of qud-", get_qud_prev["sequences"][0]["length"])
                        update_drift_value = prev_value_drift_length - (
                                update_data.get("length", 0) - get_qud_prev["sequences"][0].get("length", 0))
                        print("new vlaue of drift is ", update_drift_value)
                        result = database.update_one(
                            {"id": str(id)},
                            {"$set": {"sequences.$[element].length": update_drift_value}},
                            array_filters=[{"element.index": int(target_drift), "element.type": "Drift"}]
                        )

                    if result.modified_count > 0:
                        print("Sequence updated successfully")
                        is_sequence_update = True
                    else:
                        print("Sequence not found or not updated")
                except Exception as e:
                    print("Error updating sequence:", e)

        for sequence in sequences:
            if sequence["name"] == quad_name:
                print("Sequence found with name:", quad_name)
                database.update_one(
                    {"id": str(id), "sequences.name": quad_name},
                    {"$set": {"sequences.$": update_data}}
                )

                database.update_one(
                    {"id": str(id), "quadrupoles.name": quad_name},
                    {"$set": {f"quadrupoles.$": update_data}}
                )
                print("Quadrupole details updated successfully")
                is_quad_updated = True
                return {"message": "Quadrupole and sequence updated successfully"}

        if not is_quad_updated:
            raise HTTPException(status_code=404,
                                detail=f"Quadrupole with name {quad_name} not found in the sequence collection")
        if not is_sequence_update:
            raise HTTPException(status_code=404,
                                detail=f"Sequence with target drift {target_drift} not found in the sequence collection")
    else:
        raise HTTPException(status_code=404, detail=f"Machine with ID {id} not found")
