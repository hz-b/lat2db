from lat2db.controller.get_machine_output import get_machine

machine = get_machine(machine_id="6602a1b4ea5f066ab6e502af")
result = machine.retrieve_element_coordinate("Q5M1T1R")
result