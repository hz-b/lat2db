import json
import logging
import os
from typing import List, Dict

import jsons
from bson import ObjectId
from pymongo import MongoClient

from lat2db import mongodb_url
from lat2db.model.machine import Machine

logger = logging.getLogger('lat2db')
DB_NAME = os.environ.get("MONGODB_DB", "bessyii")
mongo_init = {'client': MongoClient(mongodb_url), 'db': MongoClient(mongodb_url)[DB_NAME]}


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
    path = get_config_filename("lat2db", file_name)
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError as exc:
        logger.error(f'Could not find package data file {file_name} using path {path}')
        raise exc


def get_config_filename(module_name: str, filename: str):
    '''Get the configuration filename using pkg_resources
    '''
    from importlib.resources import files
    path = files(module_name) / 'db' / filename
    logger.info('Config file expected at %s', path)
    return path



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
