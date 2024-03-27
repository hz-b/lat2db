from typing import List, Dict
import jsons
from bson import ObjectId
from lat2db.db.mongo_repository import InitializeMongo
from lat2db.model.machine import Machine

mongo_init = InitializeMongo()


def get_machine(machine_id: str) -> Machine:
    machine = mongo_init.get_collection("machines").find_one({"_id": ObjectId(machine_id)})
    return jsons.load(machine, Machine)


def get_machine_element_list(machine: List[Dict], element_name: str):
    element_list = machine[f'{element_name}']
    return element_list


def filter_an_element(tags: List[str], element_list: List[Dict], element_name: str) -> Dict[str, List[Dict]]:
    result = {}
    for element in element_list:
        if any(tag in element.get('tags', []) for tag in tags):
            result.setdefault(f"{element_name}", []).append(element)
    return result


def filter_machine_element_by_tags(machine_id: str, element_name: str, tags: List[str]):
    machine = mongo_init.get_collection("machines").find_one({"_id": ObjectId(machine_id)})
    element_list = machine[f'{element_name}']
    return filter_an_element(tags, element_list, element_name)


def filter_element_by_tags(machine: List[Dict], element_name: str, tags: List[str]):
    element_list = machine[f'{element_name}']
    return filter_an_element(tags, element_list, element_name)
