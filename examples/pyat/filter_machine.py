# read them
from lat2db.controller.get_machine_output import get_machine, get_machine_element_list, filter_an_element, \
    filter_machine_element_by_tags

# this way you can get filtered fields for each element type e.g. quadrupoles, sextupoles, bendings.
# the element names are always small letters as this is getting it from model where python naming convention is used
filtered_quads = filter_machine_element_by_tags(machine_id="7fb258b7-679e-4a53-9f23-9d7e7d36b932",
                                                element_name="quadrupoles", tags=["Q1"])

filtered_sextupoles = filter_machine_element_by_tags(machine_id="7fb258b7-679e-4a53-9f23-9d7e7d36b932",
                                                element_name="sextupoles", tags=["V"])

filtered_bending= filter_machine_element_by_tags(machine_id="7fb258b7-679e-4a53-9f23-9d7e7d36b932",
                                                element_name="bendings", tags=["V"])