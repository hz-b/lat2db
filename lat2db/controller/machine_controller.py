from typing import List

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from lat2db.model.machine import Machine
from lat2db.model.update_machine import MachineUpdate

router = APIRouter()

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
