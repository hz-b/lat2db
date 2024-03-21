from lat2db.controller.get_machine_output import get_machine

machine = get_machine(machine_id="65f96b620bdd4bc72d87dd93")
result = machine.retrieve_element_coordinate("Q5M1T1R")
result