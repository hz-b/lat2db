
from itertools import chain
from pymongo import MongoClient
import sys
sys.path.append('/Users/safiullahomar/lattice/lat2db test')
from lat2db.model.quadrupole import Quadrupole
from lat2db.model.sextupole import Sextupole
from lat2db.model.drift import Drift
from lat2db.model.bending import Bending
from lat2db.model.marker import Marker
from lat2db.model.horizontal_steerer import HorizontalSteerer
from lat2db.model.vertical_steerer import VerticalSteerer
from lat2db.model.beam_position_monitor import BeamPositionMonitor
from lat2db.model.cavity import Cavity
from lat2db.model.version import Version
from lat2db.model.dipole import Dipole
from lat2db.model.monitor import Monitor
import uuid
from dataclasses import dataclass, fields


from lat2db.tools.pyat.bessy2_export import bessy2Lattice

    #new database by name of db1


def insert_elements(ring, parent_id=None):
        
        client = MongoClient('mongodb://localhost:27017/')
        db = client['db1']
        collection = db['machines']

            #previosu machine databasse and its collection
        client_bess = MongoClient('mongodb://localhost:27017/')
        db_bess = client_bess['bessyii']
        collection_bess = db_bess['machines']


        all_elements = []
        quad_elements=[]
        sextupole_elements=[]
        drift_elements=[]

        bending_elements=[]
        marker_elements=[]
        h_steerer_elements=[]
        v_steerer_elements=[]
        beamposition_elements=[]
        cavity_elements=[]
        version_elements=[]
        dipole_elements=[]
        monitor_elements=[]










        index=0
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
            element_str = str(element)
            
            lines = element_str.split('\n')
            
            element_data = {}
            element_quad={}
            element_sextupole={}
            element_drift={}

            element_bending={}
            element_marker={}
            element_h_steerer={}
            element_v_steerer={}
            element_beamposition={}
            element_cavity={}
            element_version={}
            element_dipole={}
            element_monitor={}

            line_number=1
            typename=""
            changesnumber=0

            for line in lines:
                if line.strip() == '':
                    continue
                

                key, value = line.split(':', 1)
                if line_number==1:
                    value=key
                    key="type"
                    line_number+=1
                    typename=value
                if key.lower()=="famname":
                    print(key.lower())
                    key="name"
                key = key.lower().strip()
                value = value.strip()
              
                element_data[key] = value
                element_quad[key] = value
                element_sextupole[key]=value
                element_drift[key]=value

                element_bending[key]=value
                element_marker[key]=value
                element_h_steerer[key]=value
                element_v_steerer[key]=value
                element_beamposition[key]=value
                element_cavity[key]=value
                element_version[key]=value
                element_dipole[key]=value
                element_monitor[key]=value


            if typename.lower() == "quadrupole":
               
                for field in quadrupole_fields:
                    if field not in element_quad:
                        # Add missing property with null value
                        element_quad[field] = None
                        
                # Store Quadrupole data separately
                #quadrupole_data = element_data
                 
            if typename.lower() == "sextupole":
                for field in sextupole_fields:
                    if field not in element_sextupole:
                        # Add missing property with null value
                        element_sextupole[field] = None
            if typename.lower() == "drift":
                for field in drift_fields:
                    if field not in element_drift:
                        # Add missing property with null value
                        element_drift[field] = None

            if typename.lower() == "bending":
                for field in bending_fields:
                    if field not in element_bending:
                        # Add missing property with null value
                        element_bending[field] = None
            if typename.lower() == "marker":
                for field in marker_fields:
                    if field not in element_marker:
                        # Add missing property with null value
                        element_marker[field] = None
            if typename.lower() == "horizontalsteerer":
                for field in h_steerer_fields:
                    if field not in element_h_steerer:
                        # Add missing property with null value
                        element_h_steerer[field] = None
            if typename.lower() == "verticalsteerer":
                for field in v_steerer_fields:
                    if field not in element_v_steerer:
                        # Add missing property with null value
                        element_v_steerer[field] = None
            if typename.lower() == "monitor":
                for field in beamposition_fields:
                    if field not in element_beamposition:
                        # Add missing property with null value
                        element_beamposition[field] = None
            if typename.lower() == "rfcavity":
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
                for field in dipole_fields:
                    if field not in element_dipole:
                        # Add missing property with null value
                        element_dipole[field] = None
            if typename.lower() == "monitor":
                for field in monitor_fields:
                    if field not in element_monitor:
                        # Add missing property with null value
                        element_monitor[field] = None

            documents = collection_bess.find()
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

                break

            """ print(typename)
            print(sequence_bess)
            if sequence_bess:
                changesnumber+=1
                # Compare properties and insert missing ones
                for key, value in sequence_bess.items():
                    if key not in element_data:
                        element_data[key] = "" """
            
            element_data["index"]=index
            element_data["name"] = element_data.pop("famname")
            all_elements.append(element_data)
            if typename.lower() == "quadrupole":
                element_quad["name"] = element_quad.pop("famname")
                element_quad["index"]=index
                quad_elements.append(element_quad)
            if typename.lower() == "sextupole":
                element_sextupole["name"] = element_sextupole.pop("famname")
                element_sextupole["index"]=index

                sextupole_elements.append(element_sextupole)
            if typename.lower() == "drift":
                element_drift["name"] = element_drift.pop("famname")
                element_drift["index"]=index
                drift_elements.append(element_drift)
            
            if typename.lower() == "bending":
                element_bending["name"] = element_bending.pop("famname")
                element_bending["index"]=index
                bending_elements.append(element_bending)
            if typename.lower() == "marker":
                element_marker["name"] = element_marker.pop("famname")
                element_marker["index"]=index

                marker_elements.append(element_marker)
            if typename.lower() == "horizontalsteerer":
                element_h_steerer["name"] = element_h_steerer.pop("famname")
                element_h_steerer["index"]=index
                h_steerer_elements.append(element_h_steerer)
            if typename.lower() == "verticalsteerer":
                element_v_steerer["name"] = element_v_steerer.pop("famname")
                element_v_steerer["index"]=index
                v_steerer_elements.append(element_v_steerer)
            if typename.lower() == "monitor":
                element_beamposition["name"] = element_beamposition.pop("famname")
                element_beamposition["index"]=index
                beamposition_elements.append(element_beamposition)
            if typename.lower() == "rfcavity":
                element_cavity["name"] = element_cavity.pop("famname")
                element_cavity["index"]=index
                cavity_elements.append(element_cavity)
            if typename.lower() == "version":
                element_version["name"] = element_version.pop("famname")
                element_version["index"]=index
                version_elements.append(element_version)
            if typename.lower() == "dipole":
                element_dipole["name"] = element_dipole.pop("famname")
                element_dipole["index"]=index
                dipole_elements.append(element_dipole)
            if typename.lower() == "monitor":
                element_monitor["name"] = element_monitor.pop("famname")
                element_monitor["index"]=index
                monitor_elements.append(element_monitor)
            index+=1

        unique_id = str(uuid.uuid4())
        base_name = "bessy2Lattice"
        collection_count = collection.count_documents({})
        unique_index = collection_count + 1
        name_with_index = f"{base_name}_{unique_index}"

        collection.insert_one({"id": unique_id , "name":name_with_index, 
                               "sequences": all_elements,
                                "quadrupoles":quad_elements,
                                "sextupoles": sextupole_elements,
                                "drifts":drift_elements,
                                 #"bendings":bending_elements,
                                 "bendings":dipole_elements,
                                  "markers":marker_elements,
                                   "horizontal_steerers":h_steerer_elements,
                                    "vertical_steerers":v_steerer_elements,
                                     #"beam_position_monitors":beamposition_elements,
                                     "beam_position_monitors":beamposition_elements,
                                      "cavities":cavity_elements
                                        #"dipoles":dipole_elements,
                                
                                })
        print(f"Number of changes made: {changesnumber}")

        #insert_elements(ring)
        #print_elements(ring)
        client.close()



if __name__ == '__main__':
    
    #for inserting the database uncomment this
    ring = bessy2Lattice()  
    insert_elements(ring)
    #print(ring["Lattice"])
    #export_to_mongodb(ring, mongodb_uri, database_name, collection_name)
    print("Exported all lattice elements  to MongoDB")
    #for running the api uncomment this
    #app.run(debug=True)