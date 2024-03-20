from typing import List

import jsons
from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from lat2db.model.machine import Machine, Quadrupole,Sextupole
from lat2db.model.update_machine import MachineUpdate
from fastapi.responses import JSONResponse
from pymongo.collection import Collection
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from dataclasses import asdict

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


@router.get("/machine/{_id}", response_description="Get a single machine by id", response_model=Machine)
def find_a_machine(_id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"_id": ObjectId(_id)})) is not None:
        return machine

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {_id} not found")


#get all Quads
@router.get("/machine/{id}/quad", response_description="Get a single machine by id", response_model=List[Quadrupole])
def find_a_machine(id: str, request: Request):
    print("inside the quad get function")
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["quadrupoles"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")

#get all Sextupoles

@router.get("/machine/{id}/sextupole", response_description="Get a single machine by id", response_model=List[Sextupole])
def find_a_machine(id: str, request: Request):
    print("inside the quad get function")
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["sextupoles"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


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


""" # qudrople update

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pymongo.collection import Collection

from .models import Quadrupole  # Import your Quadrupole model

router = APIRouter() """

""" @router.get("/machine/{id}/quad", response_description="Get a single machine by id", response_model=List[Quadrupole])
def find_a_machine(id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"id": id})) is not None:
        return machine["quadrupoles"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found") """


#update Quadrupoles

class Quadrupole_request_update(BaseModel):
    affected_quad: str
    updated_data: Quadrupole

@router.put("/machine/{id}/quad/{quad_name}", response_description="Update a quadrupole's details")
def update_quadrupole_details(id: str, quad_name: str, request_body: Quadrupole_request_update,request: Request):
    print("Inside the update function ")
    database: Collection = request.app.database["machines"]
    print("pass id is  ",id)
    machine = database.find_one({"id": id})
    print("machien is ",machine)
    if machine:
        print("Found machine with ID:", id)
        if "quadrupoles" in machine:
            print("Quadrupoles field exists in the machine document")
            if "quadrupoles" in machine:
                quadrupoles_list = machine.get("quadrupoles", [])
                sequences_list = machine.get("sequences", [])
                operations=None
                difference=0
                print("######passed index is ",request_body.updated_data.index)
                for quad_index, quad in enumerate(quadrupoles_list):
                    print("quad indexis ",quad_index)
                    if quad.get("name") == request_body.updated_data.name:  # Replace 'desired_index' with the index you want to remove
                        quad_length=quad.get("length")
                        if float(quad_length)>float(request_body.updated_data.length):
                            operations="+"
                            difference=float(quad_length)-float(request_body.updated_data.length)
                        else:
                            operations="-"
                            difference=float(request_body.updated_data.length)-float(quad_length)

                        removed_quadrupole = quadrupoles_list.pop(quad_index)
                        update_data_dict = request_body.updated_data
                        print("&&&&&&&& removed ",removed_quadrupole)
                        print("Type of update_data_dict:", type(request_body.updated_data))
                        print("Attributes of update_data_dict:", dir(request_body.updated_data))
                        

                        print("^^^^^^^^^^^^ json converted",asdict(request_body.updated_data))
                        quadrupoles_list.insert(quad_index, asdict(request_body.updated_data))
                        print("inserted.")
                        break
               
                
                database.update_one({"id": id}, {"$set": {"quadrupoles": quadrupoles_list}})
                if request_body.affected_quad!="-1":
                    for quad_index, quad in enumerate(quadrupoles_list):
                        if int(quad.get("index")) == int(request_body.affected_quad):
                            if operations == "+":
                                quad["length"] = float(quad.get("length")) + difference
                            else:
                                quad["length"] = float(quad.get("length")) - difference

                    database.update_one({"id": id}, {"$set": {"quadrupoles": quadrupoles_list}})


                return JSONResponse(status_code=200,content={"message": f"Quadrupole updated"})


#update Sextuploles
            
class Sextupole_request_update(BaseModel):
    affected_sext: str
    updated_data: Sextupole

@router.put("/machine/{id}/sext/{sext_name}", response_description="Update a sextupole's details")
def update_sextupole_details(id: str, sext_name: str, request_body: Sextupole_request_update,request: Request):
    print("Inside the update function ")
    database: Collection = request.app.database["machines"]
    print("pass id is  ",id)
    machine = database.find_one({"id": id})
    print("machien is ",machine)
    if machine:
        print("Found machine with ID:", id)
        if "sextupoles" in machine:
            print("sextupoles field exists in the machine document")
            if "sextupoles" in machine:
                sextupole_list = machine.get("sextupoles", [])
                operations=None
                difference=0
                print("######passed index is ",request_body.updated_data.index)
                for sext_index, sext in enumerate(sextupole_list):
                    print("sext indexis ",sext_index)
                    if sext.get("name") == request_body.updated_data.name:  
                        sext_length=sext.get("length")
                        if float(sext_length)>float(request_body.updated_data.length):
                            operations="+"
                            difference=float(sext_length)-float(request_body.updated_data.length)
                        else:
                            operations="-"
                            difference=float(request_body.updated_data.length)-float(sext_length)

                        removed_sextupoles = sextupole_list.pop(sext_index)
                        update_data_dict = request_body.updated_data
                        print("&&&&&&&& removed ",removed_sextupoles)
                        print("Type of update_data_dict:", type(request_body.updated_data))
                        print("Attributes of update_data_dict:", dir(request_body.updated_data))
                        

                        print("^^^^^^^^^^^^ json converted",asdict(request_body.updated_data))
                        sextupole_list.insert(quad_index, asdict(request_body.updated_data))
                        print("inserted.")
                        break
               
                
                database.update_one({"id": id}, {"$set": {"sextupoles": sextupole_list}})
                if request_body.affected_quad!="-1":
                    for sext_index, sext in enumerate(sextupole_list):
                        if int(sext.get("index")) == int(request_body.affected_quad):
                            if operations == "+":
                                sext["length"] = float(sext.get("length")) + difference
                            else:
                                sext["length"] = float(sext.get("length")) - difference

                    database.update_one({"id": id}, {"$set": {"sextupoles": sextupole_list}})


                return JSONResponse(status_code=200,content={"message": f"Sextupoles updated"})


# get the relevenet quad detail from sequence lsit
@router.get("/machine/{id}/get_quad_from_seq/{quad_name}", response_description="listing the quad from sequence")
def get_quadrupole_details_from_sequence(id: str, quad_name: str, request: Request):
    print("Inside the update function ")

    database: Collection = request.app.database[
        "machines"]  # Assuming sequence is a record in the "machines" collection

    machine = database.find_one({"id": id})  # Find the machine record by ID

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

    machine = database.find_one({"id": id})  # Find the machine id
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
                        {"id": id, "sequences": {"$elemMatch": {"name": quad_name, "type": "Quadrupole"}}},
                        projection={"sequences.$": 1}
                    )

                    print("--object of qud for the previous value ", get_qud_prev)
                    if get_qud_prev["sequences"][0]["length"] > update_data["length"]:
                        print("target drift", target_drift)
                        drift_value = database.find_one(
                            {"id": id, "sequences": {"$elemMatch": {"index": int(target_drift), "type": "Drift"}}},
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
                            {"id": id},
                            {"$set": {"sequences.$[element].length": update_drift_value}},
                            array_filters=[{"element.index": int(target_drift), "element.type": "Drift"}]
                        )
                        print("updated--------")

                    else:
                        drift_value = database.find_one(
                            {"id": id, "sequences": {"$elemMatch": {"index": int(target_drift), "type": "Drift"}}},
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
                            {"id": id},
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
                    {"id": id, "sequences.name": quad_name},
                    {"$set": {"sequences.$": update_data}}
                )

                database.update_one(
                    {"id": id, "quadrupoles.name": quad_name},
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
