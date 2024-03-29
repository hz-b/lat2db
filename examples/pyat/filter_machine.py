# read them
from lat2db.controller.get_machine_output import get_machine, filter_element_by_tags, filter_machine_element_by_tags

# this way you can get filtered fields for each element type e.g. quadrupoles, sextupoles, bendings.
# the element names are always small letters as this is getting it from model where python naming convention is used
filtered_quads = filter_machine_element_by_tags(machine_id="6602a1b4ea5f066ab6e502af",
                                                element_name="quadrupoles", tags=["Q1"])

filtered_sextupoles = filter_machine_element_by_tags(machine_id="6602a1b4ea5f066ab6e502af",
                                                     element_name="sextupoles", tags=["V"])

filtered_bending = filter_machine_element_by_tags(machine_id="6602a1b4ea5f066ab6e502af",
                                                  element_name="bendings", tags=["V"])

machine = get_machine(machine_id="6602a1b4ea5f066ab6e502af")
result = filter_element_by_tags(machine=machine, element_name="quadrupoles", tags=["Q1"])
result