import at

from lat2db.model.accelerator import Accelerator

acc = Accelerator(from_json=True) # create accelerator
"""
@INFO: Read it to Understand it:
   create accelerator from 
   Accelerator()
   This will create an accelerator by pulling first lattice object from database
   
   Accelerator(uid="put the object id from the mongodb record you want to get e.g: 662f83c50019a6f1a5ce7ea2")
   This will get the exact lattice from database
   
   Accelerator(from_json=True)
   This will pull the lattice from file: "bessyii_lattice_json.json" which must be stored in the same directory 
    
   Accelerator(fiel_name= "mls_lattice_json.json", from_json=True)
   This will pull the lattice from file: "mls_lattice_json.json" or any file name which is provided 
   and it must be stored in the same directory
   
"""
# you can also provide the string of objectId field from your mongo record to extract
#a specific lattice from db. or send name of a json file which is in the same folder e.g
# if no arguments provided then it will get the first lattice from the database if there are more then one.

element_coordinate = acc.machine.retrieve_element_coordinate("Q5M1T1R") #examine and see what is available in element coordinate
filter_res_h = acc.machine.filter_element_by_tags("quadrupoles",["Q2"]) # this will filter all quads with tags Q2
# todo: ask me what does filter by tags mean we can expand the filters
filter_res_v = acc.machine.filter_element_by_tags("sextupoles",["V"])
orbit = acc.ring.find_orbit(at.All) # call find orbit from AT

twiss = acc.ring.get_optics(at.All)
orbit
