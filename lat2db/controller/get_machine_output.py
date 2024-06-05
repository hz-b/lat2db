import logging
import json
import os
from typing import List, Dict

import jsons
from bson import ObjectId
from pymongo import MongoClient

from lat2db.model.machine import Machine

logger = logging.getLogger('lat2db')

try:
    mongodb_url = os.environ["MONGODB_URL"]
except KeyError:
    from lat2db import mongodb_url

    logger.info(
        'Environment variable MONGODB_URL is not defined, using default %s',  mongodb_url
    )


mongo_init = {'client': MongoClient(mongodb_url), 'db': MongoClient(mongodb_url)['bessyii']}


def get_machine(machine_id: str) -> Machine:
    machine = mongo_init['db']["machines"].find_one({"_id": ObjectId(machine_id)})
    return jsons.load(machine, Machine)


def get_machine_as_json_from_db(machine_id: str):
    if (machine_id is None):
        machine = mongo_init['db']["machines"].find_one({})
        return machine
    elif(machine := mongo_init['db']["machines"].find_one({"id": str(machine_id)})) is not None:
        return machine
    else :
        machine = mongo_init['db']["machines"].find_one({"_id": ObjectId(machine_id)})
        return machine

def get_machine_as_json(file_name):
    if (file_name is None):
        file_name = "bessyii_lattice_json.json"
    with open(file_name, 'r') as file:
        return json.load(file)


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
    machine = mongo_init['db']["machines"].find_one({"_id": ObjectId(machine_id)})
    element_list = machine[f'{element_name}']
    return filter_an_element(tags, element_list, element_name)


def filter_element_by_tags(machine: List[Dict], element_name: str, tags: List[str]):
    element_list = machine[f'{element_name}']
    return filter_an_element(tags, element_list, element_name)
