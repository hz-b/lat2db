import sys

import numpy as np
from pymongo import MongoClient

sys.path.append('/Users/safiullahomar/lattice/lat2db test')
from lat2db.model.quadrupole import Quadrupole
from lat2db.model.sextupole import Sextupole
from lat2db.model.drift import Drift
from lat2db.model.bending import Bending
from lat2db.model.marker import Marker
from lat2db.model.horizontal_steerer import HorizontalSteerer
from lat2db.model.vertical_steerer import VerticalSteerer
from lat2db.model.beam_position_monitor import BeamPositionMonitor
from lat2db.model.cavity import Cavity,RFFieldHarmonic
from lat2db.model.version import Version
from lat2db.model.dipole import Dipole
from lat2db.model.monitor import Monitor
from lat2db.model.magnetic_element import MagneticElement
from lat2db.model.magnetic_element import MultipoleCoefficients
import uuid
from dataclasses import fields

from lat2db.tools.pyat.bessy2_export import bessy2Lattice


# new database by name of db1


def insert_elements(ring, parent_id=None):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['db1']
    collection = db['machines']

    # previosu machine databasse and its collection
    client_bess = MongoClient('mongodb://localhost:27017/')
    db_bess = client_bess['bessyii']
    collection_bess = db_bess['machines']

    all_elements = []
    quad_elements = []
    sextupole_elements = []
    drift_elements = []

    bending_elements = []
    marker_elements = []
    h_steerer_elements = []
    v_steerer_elements = []
    beamposition_elements = []
    cavity_elements = []
    version_elements = []
    dipole_elements = []
    monitor_elements = []

    index = 0
    quadrupole_data = {}  # Store Quadrupole data separately
    # Get all fields of the Quadrupole class
    quadrupole_fields = [field.name for field in fields(Quadrupole)]
    sextupole_fields = [field.name for field in fields(Sextupole)]
    drift_fields = [field.name for field in fields(Drift)]

    bending_fields = [field.name for field in fields(Bending)]
    marker_fields = [field.name for field in fields(Marker)]
    h_steerer_fields = [field.name for field in fields(HorizontalSteerer)]
    v_steerer_fields = [field.name for field in fields(VerticalSteerer)]
    beamposition_fields = [field.name for field in fields(BeamPositionMonitor)]
    cavity_fields = [field.name for field in fields(Cavity)]
    version_fields = [field.name for field in fields(Version)]
    dipole_fields = [field.name for field in fields(Dipole)]
    monitor_fields = [field.name for field in fields(Monitor)]

    for element in ring:

        element_fields = set(vars(element).keys())

        element_str = str(element)

        element_split_by_space = element_str.split('\n')

        element_data = {}
        element_quad = {}
        element_sextupole = {}
        element_drift = {}

        element_bending = {}
        element_marker = {}
        element_h_steerer = {}
        element_v_steerer = {}
        element_beamposition = {}
        element_cavity = {}
        element_version = {}
        element_dipole = {}
        element_monitor = {}

        _row = 1
        typename = ""
        changesnumber = 0

        for row_in_split in element_split_by_space:

            if row_in_split.strip() == '':
                continue
            
            if _row==1:

                pass
            else:
                break

            key, value = row_in_split.split(':', 1)
            if _row == 1:
                value = key
                key = "type"
                _row += 1
                typename = value
                # key = key.lower().strip()
                # value = value.strip()
                # element_data[key] = value
            if key.lower() == "famname":
                print(key.lower())
                key = "name"

            key = key.lower().strip()
            value = value.strip()

            #element_data[key] = value
            if typename.lower() == "quadrupole":
                element_quad[key] = value
            if typename.lower() == "sextupole":
                element_sextupole[key] = value
            if typename.lower() == "drift":
                element_drift[key] = value
            if typename.lower() == "bending":
                element_bending[key] = value
            if typename.lower() == "marker":
                element_marker[key] = value
            if typename.lower() == "horizontalsteerer":
                element_h_steerer[key] = value
            if typename.lower() == "verticalsteerer":
                element_v_steerer[key] = value
            if typename.lower() == "monitor":
                element_beamposition[key] = value
            if typename.lower() == "rfcavity":
                element_cavity[key] = value
            if typename.lower() == "version":
                element_version[key] = value
            if typename.lower() == "dipole":
                element_dipole[key] = value
            if typename.lower() == "monitor2":
                element_monitor[key] = value


        type_to_element_data = {
        "monitor2": element_monitor,
        "dipole": element_dipole,
        "quadrupole": element_quad,
        "sextupole": element_sextupole,
        "drift": element_drift,
        "bending": element_bending,
        "marker": element_marker,
        "horizontalsteerer": element_h_steerer,
        "verticalsteerer": element_v_steerer,
        "monitor": element_beamposition,
        "rfcavity": element_cavity,
        "version": element_version
        }
        element_data_dict = type_to_element_data.get(typename.lower())



        for field in element_fields:


            field_value = getattr(element, field)
            if isinstance(field_value, np.ndarray):
                # If the field value is a NumPy array, convert it to a list
                field_value = field_value.tolist()
            # Assign the field value to element_data
            
            if typename.lower() == "monitor2":
                element_monitor[field] = field_value
            if typename.lower() == "dipole":
                element_dipole[field] = field_value

            if typename.lower() == "rfcavity":
                element_cavity[field] = field_value
            if typename.lower() == "monitor":
                element_beamposition[field] = field_value

            if typename.lower() == "verticalsteerer":
                element_v_steerer[field] = field_value
            if typename.lower() == "horizontalsteerer":
                element_h_steerer[field] = field_value
            

            if typename.lower() == "verticalsteerer":
                element_v_steerer[field] = field_value
            if typename.lower() == "horizontalsteerer":
                element_h_steerer[field] = field_value

            if typename.lower() == "marker":
                element_marker[field] = field_value
            if typename.lower() == "bending":
                element_bending[field] = field_value
            
            if typename.lower() == "drift":
                element_drift[field] = field_value
            if typename.lower() == "sextupole":
                element_sextupole[field] = field_value
            
            if typename.lower() == "quadrupole":
                element_quad[field] = field_value
            


        if typename.lower() == "quadrupole":
            element_quad["main_multipole_strength"] = element_quad.pop("k", None)
            # element_quad["passmethod"] = element_quad.pop("method")
            multipole_coefficients = MultipoleCoefficients()
            multipole_coefficients.normal_coefficients = [float(x) for x in element_quad.pop("PolynomA")]
            multipole_coefficients.skew_coefficients = [float(x) for x in element_quad.pop("PolynomB")]
            magnetic_element = MagneticElement(coeffs=multipole_coefficients,passmethod=element_quad.pop("PassMethod"))
            element_quad["element_properties"] = magnetic_element.to_dict()
            element_quad["number_of_integration_steps"] = element_quad.pop("NumIntSteps", None)
            element_quad["name"] = element_quad.pop("FamName", None)
            element_quad["length"] = element_quad.pop("Length", None)

            for field in quadrupole_fields:
                if field not in element_quad:
                    # Add missing property with null value
                    element_quad[field] = None

            # Store Quadrupole data separately
            # quadrupole_data = element_data

        if typename.lower() == "sextupole":
            
            multipole_coefficients = MultipoleCoefficients()
            multipole_coefficients.normal_coefficients = [float(x) for x in element_sextupole.pop("PolynomA")]
            multipole_coefficients.skew_coefficients = [float(x) for x in element_sextupole.pop("PolynomB")]
            magnetic_element = MagneticElement(coeffs=multipole_coefficients,passmethod=element_sextupole.pop("PassMethod"))
            element_sextupole["element_properties"] = magnetic_element.to_dict()
            element_sextupole["number_of_integration_steps"] = element_sextupole.pop("NumIntSteps", None)
            element_sextupole["name"] = element_sextupole.pop("FamName", None)
            element_sextupole["length"] = element_sextupole.pop("Length", None)
            for field in sextupole_fields:
                if field != "element_properties" and field not in element_sextupole:
                    # Add missing property with null value
                    element_sextupole[field] = None
           
        if typename.lower() == "drift":
            # element_drift["passmethod"] = element_quad.pop("method")
            element_drift["name"] = element_drift.pop("FamName", None)
            element_drift["length"] = element_drift.pop("Length", None)
            for field in drift_fields:
                if field not in element_drift:
                    # Add missing property with null value
                    element_drift[field] = None

        if typename.lower() == "bending":
            # element_bending["passmethod"] = element_quad.pop("method")
            element_bending["main_multipole_strength"] = element_bending.pop("k", None)
            multipole_coefficients = MultipoleCoefficients()
            multipole_coefficients.normal_coefficients = [float(x) for x in element_bending.pop("PolynomA")]
            multipole_coefficients.skew_coefficients = [float(x) for x in element_bending.pop("PolynomB")]
            magnetic_element = MagneticElement(coeffs=multipole_coefficients,passmethod=element_bending.pop("PassMethod"))
            element_bending["element_properties"] = magnetic_element.to_dict()
            element_bending["number_of_integration_steps"] = element_bending.pop("NumIntSteps", None)
            element_bending["name"] = element_bending.pop("FamName", None)
            element_bending["length"] = element_bending.pop("Length", None)


            for field in bending_fields:
                if field not in element_bending:
                    # Add missing property with null value
                    element_bending[field] = None
        if typename.lower() == "marker":
            # element_marker["passmethod"] = element_quad.pop("method")
            element_marker["name"] = element_marker.pop("FamName", None)
            element_marker["length"] = element_marker.pop("Length", None)
            for field in marker_fields:
                if field not in element_marker:
                    # Add missing property with null value
                    element_marker[field] = None
        if typename.lower() == "horizontalsteerer":
            element_h_steerer["name"] = element_h_steerer.pop("FamName", None)
            element_h_steerer["length"] = element_h_steerer.pop("Length", None)
            for field in h_steerer_fields:
                if field not in element_h_steerer:
                    # Add missing property with null value
                    element_h_steerer[field] = None
        if typename.lower() == "verticalsteerer":
            element_v_steerer["name"] = element_v_steerer.pop("FamName", None)
            element_v_steerer["length"] = element_v_steerer.pop("Length", None)
            for field in v_steerer_fields:
                if field not in element_v_steerer:
                    # Add missing property with null value
                    element_v_steerer[field] = None
        if typename.lower() == "monitor":
            element_beamposition["name"] = element_beamposition.pop("FamName", None)
            element_beamposition["length"] = element_beamposition.pop("Length", None)
            for field in beamposition_fields:
                if field not in element_beamposition:
                    # Add missing property with null value
                    element_beamposition[field] = None
        if typename.lower() == "rfcavity":
            
            
           
            """ harmonic_fields = RFFieldHarmonic(voltage=element_cavity.pop("Voltage"), 
                                              frequency=element_cavity.pop("Frequency"),
                                              energy=element_cavity.pop("Energy"),
                                              timelag=element_cavity.pop("TimeLag")
                                              ) """
            harmonic_fields_dict = {
                "voltage": element_cavity.pop("Voltage"),
                "frequency": element_cavity.pop("Frequency"),
                #"phase": element_cavity.pop("Phase"),
                "energy": element_cavity.pop("Energy"),
                "timelag": element_cavity.pop("TimeLag")
            }
            #harmonic_fields["phase"]=element_cavity.pop("Voltage")
            

            element_cavity["element_configuration"] = harmonic_fields_dict


            element_cavity["name"] = element_cavity.pop("FamName", None)
            element_cavity["harmonic_number"] = element_cavity.pop("HarmNumber", None)
            element_cavity["length"] = element_cavity.pop("Length", None)
            for field in cavity_fields:
                if field not in element_cavity:
                    # Add missing property with null value
                    element_cavity[field] = None

        if typename.lower() == "version":
            for field in version_fields:
                if field not in element_version:
                    # Add missing property with null value
                    element_version[field] = None
        if typename.lower() == "dipole":
            element_dipole["main_multipole_strength"] = element_dipole.pop("k", None)
            multipole_coefficients = MultipoleCoefficients()
            multipole_coefficients.normal_coefficients = [float(x) for x in element_dipole.pop("PolynomA")]
            multipole_coefficients.skew_coefficients = [float(x) for x in element_dipole.pop("PolynomB")]
            magnetic_element = MagneticElement(coeffs=multipole_coefficients,passmethod=element_dipole.pop("PassMethod"))
            element_dipole["element_properties"] = magnetic_element.to_dict()
            element_dipole["number_of_integration_steps"] = element_dipole.pop("NumIntSteps", None)
            element_dipole["name"] = element_bending.pop("FamName", None)
            element_dipole["length"] = element_bending.pop("Length", None)


            for field in bending_fields:
                if field not in element_dipole:
                    # Add missing property with null value
                    element_dipole[field] = None

        if typename.lower() == "monitor":
            element_monitor["name"] = element_monitor.pop("FamName", None)
            element_monitor["length"] = element_monitor.pop("Length", None)
            for field in monitor_fields:
                if field not in element_monitor:
                    # Add missing property with null value
                    element_monitor[field] = None

        """    documents = collection_bess.find()
        for document in documents:
            sequences = document.get("sequences", [])

            for sequence in sequences:
                sequence_type = sequence.get("type")

                if sequence_type == typename:
                    changesnumber += 1
                    # Compare properties and insert missing ones
                    for key, value in sequence.items():
                        if key not in element_data:
                            element_data[key] = None

            break """

        """ print(typename)
        print(sequence_bess)
        if sequence_bess:
            changesnumber+=1
            # Compare properties and insert missing ones
            for key, value in sequence_bess.items():
                if key not in element_data:
                    element_data[key] = "" """

        #element_data["index"] = index
        #element_data["name"] = element_data.pop("famname")
        #element_data["main_multipole_strength"] = element_data.pop("k", None)

        #all_elements.append(element_data)
        if typename.lower() == "quadrupole":
            #element_quad["name"] = element_quad.pop("famname")
            element_quad["index"] = index
            quad_elements.append(element_quad)
            all_elements.append(element_quad)

        if typename.lower() == "sextupole":
           # element_sextupole["name"] = element_sextupole.pop("famname")
            element_sextupole["index"] = index
            
            sextupole_elements.append(element_sextupole)
            all_elements.append(element_sextupole)

        if typename.lower() == "drift":
            #element_drift["name"] = element_drift.pop("famname")
            element_drift["index"] = index
            drift_elements.append(element_drift)
            all_elements.append(element_drift)

        if typename.lower() == "bending":
            #element_bending["name"] = element_bending.pop("famname")
            element_bending["index"] = index
            bending_elements.append(element_bending)
            print("bending elements")
            print(bending_elements)
            all_elements.append(element_bending)
        if typename.lower() == "marker":
            #element_marker["name"] = element_marker.pop("famname")
            element_marker["index"] = index

            marker_elements.append(element_marker)
            all_elements.append(element_marker)
        if typename.lower() == "horizontalsteerer":
            #element_h_steerer["name"] = element_h_steerer.pop("famname")
            element_h_steerer["index"] = index
            h_steerer_elements.append(element_h_steerer)
            all_elements.append(element_h_steerer)
        if typename.lower() == "verticalsteerer":
            #element_v_steerer["name"] = element_v_steerer.pop("famname")
            element_v_steerer["index"] = index
            v_steerer_elements.append(element_v_steerer)
            all_elements.append(element_v_steerer)
        if typename.lower() == "monitor":
            #element_beamposition["name"] = element_beamposition.pop("famname")
            element_beamposition["index"] = index
            beamposition_elements.append(element_beamposition)
            all_elements.append(element_beamposition)
        if typename.lower() == "rfcavity":
            #element_cavity["name"] = element_cavity.pop("famname")
            element_cavity["index"] = index
            cavity_elements.append(element_cavity)
            all_elements.append(element_cavity)
        if typename.lower() == "version":
            #element_version["name"] = element_version.pop("famname")
            element_version["index"] = index
            version_elements.append(element_version)
            #element_data.append(element_version)
        if typename.lower() == "dipole":
            #element_dipole["name"] = element_dipole.pop("famname")
            element_dipole["index"] = index
            dipole_elements.append(element_dipole)
            all_elements.append(element_dipole)
        """ if typename.lower() == "monitor":
            element_monitor["name"] = element_monitor.pop("famname")
            element_monitor["index"]=index
            monitor_elements.append(element_monitor) """
        index += 1

    unique_id = str(uuid.uuid4())
    base_name = "bessy2Lattice"
    collection_count = collection.count_documents({})
    unique_index = collection_count + 1
    name_with_index = f"{base_name}_{unique_index}"

    collection.insert_one({"id": unique_id, "name": name_with_index,
                           "sequences": all_elements,
                           "quadrupoles": quad_elements,
                           "sextupoles": sextupole_elements,
                           "drifts": drift_elements,
                           # "bendings":bending_elements,
                           "bendings": dipole_elements,
                           "markers": marker_elements,
                           "horizontal_steerers": h_steerer_elements,
                           "vertical_steerers": v_steerer_elements,
                           # "beam_position_monitors":beamposition_elements,
                           "beam_position_monitors": beamposition_elements,
                           "cavities": cavity_elements
                           # "dipoles":dipole_elements,

                           })
    # print(f"Number of changes made: {changesnumber}")

    # insert_elements(ring)
    # print_elements(ring)
    client.close()


if __name__ == '__main__':
    # for inserting the database uncomment this
    ring = bessy2Lattice()
    insert_elements(ring)
    # print(ring["Lattice"])
    # export_to_mongodb(ring, mongodb_uri, database_name, collection_name)
    print("Exported all lattice elements  to MongoDB")
    # for running the api uncomment this
    # app.run(debug=True)
