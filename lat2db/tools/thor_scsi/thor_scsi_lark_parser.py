
import sys
import os

sys.path.append('/Users/safiullahomar/lattice/lat2db test')

from lat2db.tools.thor_scsi.parser import MADXTransformer, parse
from importlib.resources import files
from lark import Lark
from pymongo import MongoClient
from lat2db.model.machine import Machine
from lat2db.model.marker import Marker
from lat2db.model.drift import Drift
from lat2db.model.quadrupole import Quadrupole
from lat2db.model.sextupole import Sextupole
from lat2db.model.bending import Bending
from lat2db.model.beam_position_monitor import BeamPositionMonitor
from lat2db.model.cavity import  Cavity
__all__ = ["get_lark", "to_json"]


client = MongoClient('mongodb://localhost:27017/')
db = client['bessyii_3']
collection = db['machines']

def get_lark_file():
    #return files(__name__.split(".")[0]).joinpath('tools/thor_scsi/thor_scsi.lark')
    return '/Users/safiullahomar/lattice/lat2db test/lat2db/tools/thor_scsi/thor_scsi.lark'

def get_lark():
    with open(get_lark_file(), "rt") as file:
        parser = Lark(file, parser="lalr", maybe_placeholders=True)
        #: Todo: find out why that seek
        file.seek(0)
    return parser

def to_json(lattice_content: str):
    print("called to json")
    tree = get_lark().parse(lattice_content)
    machine_data = MADXTransformer().transform(tree)
    organized_dict = parse(machine_data)
    variables = machine_data['variables']
    
    return organized_dict, variables


def main():
    
    lat_file_path = '/Users/safiullahomar/lattice/lat2db test/scripts/b2_stduser_beamports_blm_tracy_corr.lat'

    # Read the content of the .lat file
    with open(lat_file_path, 'r') as file:
        lattice_content = file.read()

    # Convert to JSON-like dictionary
    organized_dict, variables = to_json(lattice_content)




    machine = Machine(name="new_db")

    for key, element in organized_dict.items():

        print("key:-------------------------", key)
        print("Element:-------------------------", element)
        element_type=element.get("type")
        if element_type == 'Marker':
            try:
                marker_obj = Marker(**element)
                machine.add_marker(marker_obj)
                machine.add_to_sequence(marker_obj)
            except Exception as e:
                print(f"Error creating Marker: {e}")
        elif element_type == 'Bpm':
            try:
                bpm_obj = BeamPositionMonitor(**element)
                machine.add_beam_position_monitor(bpm_obj)
                machine.add_to_sequence(bpm_obj)
            except Exception as e:
                print(f"Error creating Bmp: {e}")
        elif element_type == 'Bending':
            try:
                bending_data = transform_element_data(element)
                bending_obj = Bending(**bending_data)
                machine.add_bending(bending_obj)
                machine.add_to_sequence(bending_obj)
            except Exception as e:
                print(f"Error creating Bending: {e}")
        elif element_type == 'Drift':
            try:
                drift_data = transform_element_data(element)
                drift_obj = Drift(**drift_data)
                machine.add_drift(drift_obj)
                machine.add_to_sequence(drift_obj)
            except Exception as e:
                print(f"Error creating Drift: {e}")
        elif element_type == 'Sextupole':
            try:
                sext_data = transform_element_data(element)
                sextupole_obj = Sextupole(**sext_data)
                machine.add_sextupole(sextupole_obj)
                machine.add_to_sequence(sextupole_obj)
            except Exception as e:
                print(f"Error creating Sextupole: {e}")

        elif element_type == 'Quadrupole':
            try:
                quad_data = transform_element_data(element)
                quadrupole_obj = Quadrupole(**quad_data)
                machine.add_quadrupole(quadrupole_obj)
                machine.add_to_sequence(quadrupole_obj)
            except Exception as e:
                print(f"Error creating Quadrupole: {e}")

        elif element_type == 'Cavity':
            try:
                cavi_data = transform_element_data(element)
                cavi_obj = Cavity(**cavi_data)
                machine.add_cavity(cavi_obj)
                machine.add_to_sequence(cavi_obj)
            except Exception as e:
                print(f"Error creating cavities: {e}")

    save_machine_to_mongodb(machine)


def save_machine_to_mongodb(machine):
    machine_dict = machine.to_dict()
    collection.insert_one(machine_dict)
    print(f"Machine with ID {machine.id} saved to MongoDB.")


def transform_element_data(element):
    transformed_element = element.copy()
    if 'L' in transformed_element:
        transformed_element['length'] = transformed_element.pop('L')
    if 'Method' in transformed_element:
        transformed_element['passmethod'] = transformed_element.pop('Method')

    if 'Harmonicnumber' in transformed_element:
        transformed_element['harmonic_number'] = transformed_element.pop('Harmonicnumber')

    if 'Voltage' in transformed_element:
        transformed_element['voltage'] = transformed_element.pop('Voltage')
    if 'Frequency' in transformed_element:
        transformed_element['frequency'] = transformed_element.pop('Frequency')

    return transformed_element

if __name__ == "__main__":
    main()