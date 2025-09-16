import sys

import numpy as np
from pymongo import MongoClient

from lat2db.model.octupole import Octupole
from lat2db.tools.pyat.bessy2_TL_reflat import bessy2_TL
from lat2db.tools.pyat.mls_sr_reflat import mlsLattice

sys.path.append('/Users/safiullahomar/lattice/lat2db test')
from lat2db.model.quadrupole import Quadrupole
from lat2db.model.sextupole import Sextupole
from lat2db.model.drift import Drift
from lat2db.model.bending import Bending
from lat2db.model.marker import Marker
from lat2db.model.beam_position_monitor import BeamPositionMonitor
from lat2db.model.cavity import Cavity
from lat2db.model.version import Version
from lat2db.model.monitor import Monitor
from lat2db.model.steerer import Steerer
from lat2db.model.magnetic_element import MagneticElement
from lat2db.model.magnetic_element import MultipoleCoefficients, KickAngles
import uuid


# new database by name of db1


def insert_elements(ring, parent_id=None):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mls']
    collection = db['machines']

    # previosu machine databasse and its collection
    client_bess = MongoClient('mongodb://localhost:27017/')
    db_bess = client_bess['mls']
    collection_bess = db_bess['machines']

    all_elements = []
    quad_elements = []
    sextupole_elements = []
    octupole_elements = []
    steerer_elements = []
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
    quadrupole_fields = [*Quadrupole.__fields__]
    sextupole_fields = [*Sextupole.__fields__]
    octupole_fields = [*Octupole.__fields__]
    drift_fields = [*Drift.__fields__]
    bending_fields = [*Bending.__fields__]
    marker_fields = [*Marker.__fields__]
    beamposition_fields = [*BeamPositionMonitor.__fields__]
    cavity_fields = [*Cavity.__fields__]
    version_fields = [*Version.__fields__]
    monitor_fields = [*Monitor.__fields__]
    steerer_fields = [*Steerer.__fields__]

    for element in ring:

        element_fields = set(vars(element).keys())

        element_str = str(element)

        element_split_by_space = element_str.split('\n')

        element_data = {}
        element_quad = {}
        element_sextupole = {}
        element_octupole = {}
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
        element_steerer = {}

        _row = 1
        typename = ""
        changesnumber = 0

        for row_in_split in element_split_by_space:

            if row_in_split.strip() == '':
                continue

            if _row == 1:

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

            # element_data[key] = value
            if typename.lower() == "quadrupole":
                element_quad[key] = value
            if typename.lower() == "sextupole":
                element_sextupole[key] = value
            if typename.lower() == "octupole":
                element_octupole[key] = value
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
            if typename.lower() == "corrector":
                element_steerer[key] = value

        type_to_element_data = {
            "monitor2": element_monitor,
            "dipole": element_dipole,
            "quadrupole": element_quad,
            "sextupole": element_sextupole,
            "octupole": element_octupole,
            "drift": element_drift,
            "bending": element_bending,
            "marker": element_marker,
            "horizontalsteerer": element_h_steerer,
            "verticalsteerer": element_v_steerer,
            "monitor": element_beamposition,
            "rfcavity": element_cavity,
            "version": element_version,
            "steerer": element_steerer
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
            if typename.lower() == "octupole":
                element_octupole[field] = field_value

            if typename.lower() == "quadrupole":
                element_quad[field] = field_value

            if typename.lower() == "corrector":
                element_steerer[field] = field_value

        if typename.lower() == "quadrupole":
            # element_quad["main_multipole_strength"] = element_quad.pop("k", None)
            element_quad["passmethod"] = element_quad.pop("PassMethod")
            multipole_coefficients = MultipoleCoefficients()
            multipole_coefficients.normal_coefficients = [float(x) for x in element_quad.pop("PolynomB")]
            multipole_coefficients.skew_coefficients = [float(x) for x in element_quad.pop("PolynomA")]

            kickAngles = KickAngles()
            kick_angles_dict = {
                "x": 0.0,
                "y": 0.0
            }
            if "KickAngle" in element_quad:
                float_array = [float(x) for x in element_quad.pop("KickAngle")]

                if len(float_array) >= 2:  # Ensure there are at least two values in the array
                    kickAngles.x = float_array[0]
                    kickAngles.y = float_array[1]

                kick_angles_dict = {
                    "x": kickAngles.x,
                    "y": kickAngles.y
                }
            magnetic_element = MagneticElement(coeffs=multipole_coefficients,
                                               main_multipole_strength=element_quad.pop("k", None),
                                               main_multipole_index=None
                                               # passmethod=element_sextupole.pop("PassMethod")

                                               )
            magnetic_element_dict = {
                "coeffs": {
                    "normal_coefficients": magnetic_element.coeffs.normal_coefficients,
                    "skew_coefficients": magnetic_element.coeffs.skew_coefficients
                },
                "main_multipole_index": magnetic_element.main_multipole_index,
                "main_multipole_strength": magnetic_element.main_multipole_strength
            }
            configuation_attributes = {
                "magnetic_element": magnetic_element_dict,  # No need to call to_dict()
                "kickangle": kick_angles_dict if kickAngles.x is not None or kickAngles.y is not None else None,
                "correctors": None
            }

            element_quad["element_configuration"] = configuation_attributes
            element_quad["number_of_integration_steps"] = element_quad.pop("NumIntSteps", None)
            element_quad["name"] = element_quad.pop("FamName", None)
            element_quad["length"] = element_quad.pop("Length", None)
            element_quad["tags"] = [element_quad.pop("Corrector", "")]

            for field in quadrupole_fields:
                if field not in element_quad:
                    # Add missing property with null value
                    element_quad[field] = None

            # Store Quadrupole data separately
            # quadrupole_data = element_data

        if typename.lower() == "sextupole":

            multipole_coefficients = MultipoleCoefficients()
            multipole_coefficients.normal_coefficients = [float(x) for x in element_sextupole.pop("PolynomB")]
            multipole_coefficients.skew_coefficients = [float(x) for x in element_sextupole.pop("PolynomA")]

            kickAngles = KickAngles()
            kick_angles_dict = {
                "x": 0.0,
                "y": 0.0
            }
            if "KickAngle" in element_sextupole:
                float_array = [float(x) for x in element_sextupole.pop("KickAngle")]

                if len(float_array) >= 2:  # Ensure there are at least two values in the array
                    kickAngles.x = float_array[0]
                    kickAngles.y = float_array[1]

                kick_angles_dict = {
                    "x": kickAngles.x,
                    "y": kickAngles.y
                }
            magnetic_element = MagneticElement(coeffs=multipole_coefficients,
                                               main_multipole_strength=element_sextupole.pop("k", None),
                                               main_multipole_index=None
                                               # passmethod=element_sextupole.pop("PassMethod")

                                               )
            magnetic_element_dict = {
                "coeffs": {
                    "normal_coefficients": magnetic_element.coeffs.normal_coefficients,
                    "skew_coefficients": magnetic_element.coeffs.skew_coefficients
                },
                "main_multipole_index": magnetic_element.main_multipole_index,
                "main_multipole_strength": magnetic_element.main_multipole_strength
            }
            configuation_attributes = {
                "magnetic_element": magnetic_element_dict,  # No need to call to_dict()
                "kickangle": kick_angles_dict if kickAngles.x is not None or kickAngles.y is not None else None,
                "correctors": None
            }

            element_sextupole["element_configuration"] = configuation_attributes
            element_sextupole["number_of_integration_steps"] = element_sextupole.pop("NumIntSteps", None)
            element_sextupole["name"] = element_sextupole.pop("FamName", None)
            element_sextupole["length"] = element_sextupole.pop("Length", None)

            element_sextupole["passmethod"] = element_sextupole.pop("PassMethod")
            element_sextupole["tags"] = [element_sextupole.pop("Corrector", "")]

            for field in sextupole_fields:
                if field != "element_properties" and field not in element_sextupole:
                    # Add missing property with null value
                    element_sextupole[field] = None

        if typename.lower() == "octupole":

            multipole_coefficients = MultipoleCoefficients()
            multipole_coefficients.normal_coefficients = [float(x) for x in element_octupole.pop("PolynomB")]
            multipole_coefficients.skew_coefficients = [float(x) for x in element_octupole.pop("PolynomA")]

            kickAngles = KickAngles()
            kick_angles_dict = {
                "x": 0.0,
                "y": 0.0
            }
            if "KickAngle" in element_octupole:
                float_array = [float(x) for x in element_octupole.pop("KickAngle")]

                if len(float_array) >= 2:  # Ensure there are at least two values in the array
                    kickAngles.x = float_array[0]
                    kickAngles.y = float_array[1]

                kick_angles_dict = {
                    "x": kickAngles.x,
                    "y": kickAngles.y
                }
            magnetic_element = MagneticElement(coeffs=multipole_coefficients,
                                               main_multipole_strength=element_octupole.pop("k", None),
                                               main_multipole_index=None
                                               # passmethod=element_sextupole.pop("PassMethod")

                                               )
            magnetic_element_dict = {
                "coeffs": {
                    "normal_coefficients": magnetic_element.coeffs.normal_coefficients,
                    "skew_coefficients": magnetic_element.coeffs.skew_coefficients
                },
                "main_multipole_index": magnetic_element.main_multipole_index,
                "main_multipole_strength": magnetic_element.main_multipole_strength
            }
            configuation_attributes = {
                "magnetic_element": magnetic_element_dict,  # No need to call to_dict()
                "kickangle": kick_angles_dict if kickAngles.x is not None or kickAngles.y is not None else None,
                "correctors": None
            }

            element_octupole["element_configuration"] = configuation_attributes
            element_octupole["number_of_integration_steps"] = element_octupole.pop("NumIntSteps", None)
            element_octupole["name"] = element_octupole.pop("FamName", None)
            element_octupole["length"] = element_octupole.pop("Length", None)

            element_octupole["passmethod"] = element_octupole.pop("PassMethod")
            element_octupole["tags"] = [element_octupole.pop("Corrector", "")]

            for field in octupole_fields:
                if field != "element_properties" and field not in element_octupole:
                    # Add missing property with null value
                    element_octupole[field] = None





        if typename.lower() == "corrector":
            kickAngles = KickAngles()
            kick_angles_dict = {
                "x": 0.0,
                "y": 0.0
            }
            if "KickAngle" in element_steerer:
                float_array = [float(x) for x in element_steerer.pop("KickAngle")]

                if len(float_array) >= 2:  # Ensure there are at least two values in the array
                    kickAngles.x = float_array[0]
                    kickAngles.y = float_array[1]

                kick_angles_dict = {
                    "x": kickAngles.x,
                    "y": kickAngles.y
                }
            magnetic_element = MagneticElement(coeffs={"normal_coefficients": [0, 0], "skew_coefficients": [0, 0]},
                                               main_multipole_strength=element_steerer.pop("k", None),
                                               main_multipole_index=None
                                               )
            magnetic_element_dict = {
                "coeffs": {
                    "normal_coefficients": magnetic_element.coeffs.normal_coefficients,
                    "skew_coefficients": magnetic_element.coeffs.skew_coefficients
                },
                "main_multipole_index": magnetic_element.main_multipole_index,
                "main_multipole_strength": magnetic_element.main_multipole_strength
            }
            configuation_attributes = {
                "magnetic_element": magnetic_element_dict,  # No need to call to_dict()
                "kickangle": kick_angles_dict if kickAngles.x is not None or kickAngles.y is not None else None,
                "correctors": None
            }

            element_steerer["element_configuration"] = configuation_attributes
            element_steerer["number_of_integration_steps"] = element_steerer.pop("NumIntSteps", None)
            element_steerer["name"] = element_steerer.pop("FamName", None)
            element_steerer["length"] = element_steerer.pop("Length", None)

            element_steerer["passmethod"] = element_steerer.pop("PassMethod")
            element_steerer["tags"] = [element_steerer.pop("Corrector", "")]

            for field in sextupole_fields:
                if field != "element_properties" and field not in element_steerer:
                    # Add missing property with null value
                    element_steerer[field] = None

        if typename.lower() == "drift":
            # element_drift["passmethod"] = element_quad.pop("method")
            element_drift["name"] = element_drift.pop("FamName", None)
            element_drift["length"] = element_drift.pop("Length", None)
            element_drift["passmethod"] = element_drift.pop("PassMethod")
            for field in drift_fields:
                if field not in element_drift:
                    # Add missing property with null value
                    element_drift[field] = None
        # : to dipole
        if typename.lower() == "bending":
            # element_bending["passmethod"] = element_quad.pop("method")
            element_bending["main_multipole_strength"] = element_bending.pop("k", None)
            element_bending["passmethod"] = element_bending.pop("PassMethod")
            multipole_coefficients = MultipoleCoefficients()
            multipole_coefficients.normal_coefficients = [float(x) for x in element_bending.pop("PolynomB")]
            multipole_coefficients.skew_coefficients = [float(x) for x in element_bending.pop("PolynomA")]
            magnetic_element = MagneticElement(coeffs=multipole_coefficients
                                               # passmethod=element_bending.pop("PassMethod")

                                               )

            # element_bending["element_properties"] = magnetic_element
            element_bending["number_of_integration_steps"] = element_bending.pop("NumIntSteps", None)
            element_bending["name"] = element_bending.pop("FamName", None)
            element_bending["length"] = element_bending.pop("Length", None)
            element_bending["tags"] = [element_bending.pop("Corrector", "")]

            for field in bending_fields:
                if field not in element_bending:
                    # Add missing property with null value
                    element_bending[field] = None

        if typename.lower() == "marker":
            # element_marker["passmethod"] = element_quad.pop("method")
            element_marker["name"] = element_marker.pop("FamName", None)
            element_marker["passmethod"] = element_marker.pop("PassMethod")
            element_marker["length"] = element_marker.pop("Length", None)
            element_marker["tags"] = [element_marker.pop("Corrector", "")]
            for field in marker_fields:
                if field not in element_marker:
                    # Add missing property with null value
                    element_marker[field] = None
        """ if typename.lower() == "horizontalsteerer":
            element_h_steerer["name"] = element_h_steerer.pop("FamName", None)
            element_h_steerer["length"] = element_h_steerer.pop("Length", None)
            for field in h_steerer_fields:
                if field not in element_h_steerer:
                    # Add missing property with null value
                    element_h_steerer[field] = None """
        """ if typename.lower() == "verticalsteerer":
            element_v_steerer["name"] = element_v_steerer.pop("FamName", None)
            element_v_steerer["length"] = element_v_steerer.pop("Length", None)
            for field in v_steerer_fields:
                if field not in element_v_steerer:
                    # Add missing property with null value
                    element_v_steerer[field] = None """

        if typename.lower() == "monitor":
            element_beamposition["name"] = element_beamposition.pop("FamName", None)
            element_beamposition["length"] = element_beamposition.pop("Length", None)
            element_beamposition["passmethod"] = element_beamposition.pop("PassMethod")
            element_beamposition["tags"] = [element_beamposition.pop("Corrector", "")]
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
                # "phase": element_cavity.pop("Phase"),
                "energy": element_cavity.pop("Energy"),
                "timelag": element_cavity.pop("TimeLag")
            }
            # harmonic_fields["phase"]=element_cavity.pop("Voltage")

            element_cavity["cavity_configuration"] = harmonic_fields_dict

            element_cavity["name"] = element_cavity.pop("FamName", None)
            element_cavity["passmethod"] = element_cavity.pop("PassMethod")
            element_cavity["harmonic_number"] = element_cavity.pop("HarmNumber", None)
            element_cavity["length"] = element_cavity.pop("Length", None)
            element_cavity["tags"] = [element_cavity.pop("Corrector", "")]
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
            element_dipole["passmethod"] = element_dipole.pop("PassMethod", None)
            element_dipole["tags"] = [element_dipole.pop("Corrector", "")]
            multipole_coefficients = MultipoleCoefficients()
            multipole_coefficients.normal_coefficients = [float(x) for x in element_dipole.pop("PolynomB")]
            multipole_coefficients.skew_coefficients = [float(x) for x in element_dipole.pop("PolynomA")]

            kickAngles = KickAngles()
            kick_angles_dict = {
                "x": 0.0,
                "y": 0.0
            }
            if "KickAngle" in element_dipole:
                float_array = [float(x) for x in element_dipole.pop("KickAngle")]

                if len(float_array) >= 2:  # Ensure there are at least two values in the array
                    kickAngles.x = float_array[0]
                    kickAngles.y = float_array[1]

                kick_angles_dict = {
                    "x": kickAngles.x,
                    "y": kickAngles.y
                }
            magnetic_element = MagneticElement(coeffs=multipole_coefficients,
                                               main_multipole_strength=element_dipole.pop("k", None),
                                               main_multipole_index=None
                                               # passmethod=element_sextupole.pop("PassMethod")

                                               )
            magnetic_element_dict = {
                "coeffs": {
                    "normal_coefficients": magnetic_element.coeffs.normal_coefficients,
                    "skew_coefficients": magnetic_element.coeffs.skew_coefficients
                },
                "main_multipole_index": magnetic_element.main_multipole_index,
                "main_multipole_strength": magnetic_element.main_multipole_strength
            }
            configuation_attributes = {
                "magnetic_element": magnetic_element_dict,  # No need to call to_dict()
                "kickangle": kick_angles_dict if kickAngles.x is not None or kickAngles.y is not None else None,
                "correctors": None
            }

            element_dipole["element_configuration"] = configuation_attributes
            element_dipole["number_of_integration_steps"] = element_dipole.pop("NumIntSteps", None)
            element_dipole["name"] = element_dipole.pop("FamName", None)
            element_dipole["length"] = element_dipole.pop("Length", None)
            element_dipole["fringeint1"] = element_dipole.pop("FringeInt1", None)
            element_dipole["fringeint2"] = element_dipole.pop("FringeInt2", None)
            element_dipole["fullgap"] = element_dipole.pop("FullGap", None)
            element_dipole["entranceangle"] = element_dipole.pop("EntranceAngle", None)
            element_dipole["exitangle"] = element_dipole.pop("ExitAngle", None)
            element_dipole["bending_angle"] = element_dipole.pop("BendingAngle", None)

            for field in bending_fields:
                if field not in element_dipole:
                    # Add missing property with null value
                    element_dipole[field] = None

        if typename.lower() == "monitor":
            element_monitor["name"] = element_monitor.pop("FamName", None)
            element_monitor["length"] = element_monitor.pop("Length", None)
            element_monitor["tags"] = [element_monitor.pop("Corrector", "")]
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

        # element_data["index"] = index
        # element_data["name"] = element_data.pop("famname")
        # element_data["main_multipole_strength"] = element_data.pop("k", None)

        # all_elements.append(element_data)
        if typename.lower() == "quadrupole":
            # element_quad["name"] = element_quad.pop("famname")
            element_quad["index"] = index
            quad_elements.append(element_quad)
            all_elements.append(element_quad)

        if typename.lower() == "sextupole":
            # element_sextupole["name"] = element_sextupole.pop("famname")
            element_sextupole["index"] = index

            sextupole_elements.append(element_sextupole)
            all_elements.append(element_sextupole)
        if typename.lower() == "octupole":
            # element_sextupole["name"] = element_sextupole.pop("famname")
            element_octupole["index"] = index

            octupole_elements.append(element_octupole)
            all_elements.append(element_octupole)

        if typename.lower() == "corrector":
            # element_sextupole["name"] = element_sextupole.pop("famname")
            element_steerer["index"] = index

            steerer_elements.append(element_steerer)
            all_elements.append(element_steerer)

        if typename.lower() == "drift":
            # element_drift["name"] = element_drift.pop("famname")
            element_drift["index"] = index
            element_drift["tags"] = [element_drift.pop("Corrector", "")]
            drift_elements.append(element_drift)
            all_elements.append(element_drift)

        if typename.lower() == "bending":
            # element_bending["name"] = element_bending.pop("famname")
            element_bending["index"] = index
            bending_elements.append(element_bending)
            print("bending elements")
            print(bending_elements)
            all_elements.append(element_bending)
        if typename.lower() == "marker":
            # element_marker["name"] = element_marker.pop("famname")
            element_marker["index"] = index

            marker_elements.append(element_marker)
            all_elements.append(element_marker)
        if typename.lower() == "horizontalsteerer":
            # element_h_steerer["name"] = element_h_steerer.pop("famname")
            element_h_steerer["index"] = index
            h_steerer_elements.append(element_h_steerer)
            all_elements.append(element_h_steerer)
        if typename.lower() == "verticalsteerer":
            # element_v_steerer["name"] = element_v_steerer.pop("famname")
            element_v_steerer["index"] = index
            v_steerer_elements.append(element_v_steerer)
            all_elements.append(element_v_steerer)
        if typename.lower() == "monitor":
            # element_beamposition["name"] = element_beamposition.pop("famname")
            element_beamposition["index"] = index
            beamposition_elements.append(element_beamposition)
            all_elements.append(element_beamposition)
        if typename.lower() == "rfcavity":
            # element_cavity["name"] = element_cavity.pop("famname")
            element_cavity["index"] = index
            cavity_elements.append(element_cavity)
            all_elements.append(element_cavity)
        if typename.lower() == "version":
            # element_version["name"] = element_version.pop("famname")
            element_version["index"] = index
            version_elements.append(element_version)
            # element_data.append(element_version)
        if typename.lower() == "dipole":
            # element_dipole["name"] = element_dipole.pop("famname")
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
                           # "horizontal_steerers": h_steerer_elements,
                           # "vertical_steerers": v_steerer_elements,
                           # "beam_position_monitors":beamposition_elements,
                           "beam_position_monitors": beamposition_elements,
                           "cavities": cavity_elements,
                           "closed": True,
                           "steerers": steerer_elements
                           # "dipoles":dipole_elements,

                           })
    # print(f"Number of changes made: {changesnumber}")

    # insert_elements(ring)
    # print_elements(ring)
    client.close()


if __name__ == '__main__':
    # for inserting the database uncomment this
    ring = mlsLattice()
    insert_elements(ring)
    print(ring["Lattice"])
    # export_to_mongodb(ring, mongodb_uri, database_name, collection_name)
    print("Exported all lattice elements  to MongoDB")
    # for running the api uncomment this
    # app.run(debug=True)
