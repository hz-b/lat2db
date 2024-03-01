from typing import List

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from lat2db.model.machine import Machine, Quadrupole
from lat2db.model.update_machine import MachineUpdate
from fastapi.responses import JSONResponse
from pymongo.collection import Collection
from fastapi.encoders import jsonable_encoder

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
    if (machine := request.app.database["machines"].find_one({"id": id})) is not None:
        return machine

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


@router.get("/machine/{id}/quad", response_description="Get a single machine by id", response_model=List[Quadrupole])
def find_a_machine(id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"id": id})) is not None:
        return machine["quadrupoles"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


@router.put("/machine/{id}", response_description="Update a machine", response_model=Machine)
def update_machine(id: str, request: Request, machine: MachineUpdate = Body(...)):
    machine = {k: v for k, v in machine.dict().items() if v is not None}

    if len(machine) >= 1:
        update_result = request.app.database["machines"].update_one(
            {"_id": id}, {"$set": machine}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")

    if (
            existing_machine := request.app.database["machines"].find_one({"_id": id})
    ) is not None:
        return existing_machine

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


@router.delete("/machine/{id}", response_description="Delete a machine")
def delete_machine(id: str, request: Request, response: Response):
    delete_result = request.app.database["machines"].delete_one({"_id": id})

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


@router.put("/machine/{id}/quad/{quad_name}", response_description="Update a quadrupole's details")
def update_quadrupole_details(id: str, quad_name: str, update_data: Quadrupole, request: Request):
    print("Inside the update function ")
    database: Collection = request.app.database["machines"]

    machine = database.find_one({"id": id})

    if machine:
        print("Found machine with ID:", id)
        if "quadrupoles" in machine:
            print("Quadrupoles field exists in the machine document")
            quadrupole_index = next(
                (index for index, quad in enumerate(machine["quadrupoles"]) if quad["name"] == quad_name), None)

            if quadrupole_index is not None:
                update_data_dict = jsonable_encoder(update_data)
                print(f"The passed update data is: {update_data}")

                database.update_one(
                    {"id": id, "quadrupoles.name": quad_name},
                    {"$set": {f"quadrupoles.{quadrupole_index}": update_data_dict}}
                )
                print("Quadrupole details updated successfully")
                return JSONResponse(content={"message": "Quadrupole details updated successfully"})

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Quadrupole with name {quad_name} not found for machine with ID {id}")


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
