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
from lat2db.controller.machine_helper import MagnetUpdateRequest,update_magnet_details,ElementUpdateRequest,update_element_details,get_section_name
from datetime import datetime

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
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        machine_data = request.app.database["machines"].find_one({"id": str(id)})
        section_names = set()
        for key, value in machine_data.items():
            if isinstance(value, list):
                for item in value:
                    section_name = get_section_name(item['name'])
                    if section_name:
                        section_names.add(section_name)

    
        relevant_elements = []

        for key, value in machine_data.items():
            if isinstance(value, list):
                for item in value:
                    section_name = get_section_name(item['name'])
                    if section_name == "D3":
                        relevant_elements.append(item)
           
        
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



@router.put("/machine/{id}/quad/{quad_name}", response_description="Update a quadrupole's details")
def update_quadrupole_details(id: str, quad_name: str, request_body: MagnetUpdateRequest, request: Request):
    return update_magnet_details(id, quad_name, request_body, "quadrupoles", request)


@router.put("/machine/{id}/quad_copy/{quad_name}", response_description="Update a quadrupole's details")
def update_quadrupole_details_copy(id: str, quad_name: str, request_body: MagnetUpdateRequest, request: Request):
    database: Collection = request.app.database["machines"]
    machine = database.find_one({"id": str(id)})
    if machine:
        machine_copy = deepcopy(machine)
        pre_id = str(uuid4()) 
        current_date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        
        machine_copy["id"] = pre_id
        old_name = machine_copy.pop("name")
        machine_copy["name"] = f"{old_name}_{current_date_time}"
        database.insert_one(machine_copy)
        return update_magnet_details(pre_id, quad_name, request_body, "quadrupoles", request)


# get all Sextupoles

@router.get("/machine/{id}/sextupole", response_description="Get a single machine by id",
            response_model=List[Sextupole])
def find_a_machine(id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["sextupoles"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")


# update Sextuploles

@router.put("/machine/{id}/sext/{sext_name}", response_description="Update a sextupole's details")
def update_sextupole_details(id: str, sext_name: str, request_body: MagnetUpdateRequest, request: Request):
    return update_magnet_details(id, sext_name, request_body, "sextupoles", request)


# update sextupole copy
@router.put("/machine/{id}/sext_copy/{sext_name}", response_description="Update a sextupole's details")
def update_sextupole_details_copy(id: str, sext_name: str, request_body: MagnetUpdateRequest, request: Request):
    database: Collection = request.app.database["machines"]
    machine = database.find_one({"id": str(id)})
    if machine:
        machine_copy = deepcopy(machine)
        pre_id = str(uuid4())  
        machine_copy["id"] = pre_id
        old_name = machine_copy.pop("name")
        current_date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        machine_copy["name"] = f"{old_name}_{current_date_time}"  
        database.insert_one(machine_copy)
        return update_magnet_details(pre_id, sext_name, request_body, "sextupoles", request)


# update other elements

@router.put("/machine/{id}/drift/{drift_name}", response_description="Update a Drift's details")
def update_drift_details(id: str, drift_name: str, request_body: ElementUpdateRequest, request: Request):
    
    return update_element_details(id, drift_name, "drifts", request_body, request)

@router.put("/machine/{id}/marker/{marker_name}", response_description="Update a marker's details")
def update_marker_details(id: str, marker_name: str, request_body: ElementUpdateRequest, request: Request):
    return update_element_details(id, marker_name,"markers" ,request_body, request)


@router.put("/machine/{id}/monitor/{monitor_name}", response_description="Update a monitor's details")
def update_monitor_details(id: str, monitor_name: str, request_body: ElementUpdateRequest, request: Request):
    return update_element_details(id, monitor_name,"beam_position_monitors",request_body, request)


# get all Drifts

@router.get("/machine/{id}/drifts", response_description="Get a single machine by id", response_model=List[Drift])
def find_a_machine(id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["drifts"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")



# get all Markers

@router.get("/machine/{id}/markers", response_description="Get a single machine by id", response_model=List[Marker])
def find_a_machine(id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["markers"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")



# get all Monitors

@router.get("/machine/{id}/monitors", response_description="Get a single machine by id",
            response_model=List[BeamPositionMonitor])
def find_a_machine(id: str, request: Request):
    if (machine := request.app.database["machines"].find_one({"id": str(id)})) is not None:
        return machine["beam_position_monitors"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Machine with ID {id} not found")



# get the relevenet quad detail from sequence lsit
@router.get("/machine/{id}/get_quad_from_seq/{quad_name}", response_description="listing the quad from sequence")
def get_quadrupole_details_from_sequence(id: str, quad_name: str, request: Request):

    database: Collection = request.app.database[
        "machines"]  

    machine = database.find_one({"id": str(id)})  

    if machine:
        sequences = machine.get("sequences", [])
        for sequence in sequences:

            if sequence["name"] == quad_name:  

                return sequence

    raise HTTPException(status_code=404,
                        detail=f"Quadrupole with name {quad_name} not found in the sequence collection")


@router.put("/machine/{id}/update_quad_from_seq/{quad_name}", response_description="Update a quadrupole from sequence")
def update_quadrupole_from_sequence(id: str, target_drift: str, quad_name: str, update_data: dict, request: Request):
    database: Collection = request.app.database["machines"]

    machine = database.find_one({"id": str(id)})  # Find the machine id
    if machine:
        sequences = machine.get("sequences", [])
        is_sequence_update = False
        is_quad_updated = False
        for sequence in sequences:
            if str(sequence["index"]) == target_drift and sequence["type"] == "Drift":
                try:
                    get_qud_prev = database.find_one(
                        {"id": str(id), "sequences": {"$elemMatch": {"name": quad_name, "type": "Quadrupole"}}},
                        projection={"sequences.$": 1}
                    )

                    if get_qud_prev["sequences"][0]["length"] > update_data["length"]:
                        drift_value = database.find_one(
                            {"id": str(id),
                             "sequences": {"$elemMatch": {"index": int(target_drift), "type": "Drift"}}},
                            projection={"sequences.$": 1}
                        )
                        drift_object = drift_value["sequences"][0]

                        prev_value_drift_length = drift_object.get("length", "Length not found")
                        update_drift_value = prev_value_drift_length + (
                                get_qud_prev["sequences"][0].get("length", 0) - update_data.get("length", 0))
                      
                        result = database.update_one(
                            {"id": str(id)},
                            {"$set": {"sequences.$[element].length": update_drift_value}},
                            array_filters=[{"element.index": int(target_drift), "element.type": "Drift"}]
                        )

                    else:
                        drift_value = database.find_one(
                            {"id": str(id),
                             "sequences": {"$elemMatch": {"index": int(target_drift), "type": "Drift"}}},
                            projection={"sequences.$": 1}
                        )

                        drift_object = drift_value["sequences"][0]
                        prev_value_drift_length = drift_object.get("length", "Length not found")
                     
                        update_drift_value = prev_value_drift_length - (
                                update_data.get("length", 0) - get_qud_prev["sequences"][0].get("length", 0))
                        result = database.update_one(
                            {"id": str(id)},
                            {"$set": {"sequences.$[element].length": update_drift_value}},
                            array_filters=[{"element.index": int(target_drift), "element.type": "Drift"}]
                        )

                    if result.modified_count > 0:
                        is_sequence_update = True
                    else:
                        pass
                except Exception as e:
                    print("Error updating sequence:", e)

        for sequence in sequences:
            if sequence["name"] == quad_name:
                database.update_one(
                    {"id": str(id), "sequences.name": quad_name},
                    {"$set": {"sequences.$": update_data}}
                )

                database.update_one(
                    {"id": str(id), "quadrupoles.name": quad_name},
                    {"$set": {f"quadrupoles.$": update_data}}
                )
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


# find groups in machine db
@router.get("/machine/{id}/groups", response_description="Get machine groups", response_model=List[str])
def find_groups_in_machine(id: str, request: Request):
    machine = request.app.database["machines"].find_one({"id": str(id)})
    if machine is not None:
        section_names = set()
        for key, value in machine.items():
            
            count=0
            if isinstance(value, list):
                for item in value:
                    if count<50:
                        count=count+1
                    section_name = get_section_name(item['name'])
                    if section_name:
                        section_names.add(section_name)
        
        if section_names:
            return list(section_names)
    
    raise HTTPException(status_code=404, detail="There is no group in the collections")


# create sunburst plot 

@router.get("/machine/{id}/sunburst", response_description="Get machine burst data")
def create_sunburst_in_machine(id: str, request: Request):
    machine = request.app.database["machines"].find_one({"id": str(id)})
    if machine is not None:
        section_dict = {}
        for key, value in machine.items():
            if isinstance(value, list):
                for item in value:
                    section_name = get_section_name(item['name'])
                    element_type=item['type']
                    if section_name:
                        if section_name not in section_dict:
                            section_dict[section_name] = {}
                        if element_type not in section_dict[section_name]:
                            section_dict[section_name][element_type]=[]
                        section_dict[section_name][element_type].append(item)

        data = {
            "name": "root",
            "children": [
                {
                    "name": section,
                    "children": [
                        {
                            "name": element_type,
                            "value":1
                        }
                        for element_type, items in element_types.items()
                    ]
                }
                for section, element_types in section_dict.items()
            ]
        }

        return data
    
    raise HTTPException(status_code=404, detail="There is no group in the collections")


# create child element plot
@router.get("/machine/{id}/sunburst_children", response_description="Get burst children from chart")
def fetch_sunburst_children_in_machine(id: str, section: str, element_type: str, request: Request):
    machine = request.app.database["machines"].find_one({"id": str(id)})
    if machine is not None:
        section_dict = {}
        for key, value in machine.items():
            if isinstance(value, list):
                for item in value:
                    section_name = get_section_name(item['name'])
                    etype = item['type']
                    if section_name:
                        if section_name not in section_dict:
                            section_dict[section_name] = {}
                        if etype not in section_dict[section_name]:
                            section_dict[section_name][etype] = []
                        section_dict[section_name][etype].append(item)

        if section in section_dict and element_type in section_dict[section]:
            children = section_dict[section][element_type]
            hierarchical_data = {
                "name": element_type,
                "children": []
            }
            for child in children:
                hierarchical_data["children"].append({
                    "name": child["name"],
                    "index":child["index"],
                    "value":1
                })
            return hierarchical_data

    raise HTTPException(status_code=404, detail="Machine not found")

#find the element in group

@router.get("/machine/{id}/relevant_elements/groups/{section_name}", response_description="Get relevant elements from groups", response_model=List[dict])
def find_elements_in_groups(id: str, section_name: str, request: Request):
    machine = request.app.database["machines"].find_one({"id": id})
    if machine is not None:
        relevant_elements = []
        for key, value in machine.items():
            if isinstance(value, list):
                for item in value:
                    item_section_name = get_section_name(item['name'])
                    if item_section_name == section_name:
                        relevant_elements.append(item)  

        if relevant_elements:
            return relevant_elements
    
    raise HTTPException(status_code=404, detail="There is no element in the section")

    

        
    