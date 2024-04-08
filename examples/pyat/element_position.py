from lat2db.controller.get_machine_output import get_machine

machine = get_machine(machine_id="660cfbde6507650b2d41a49e")
result = machine.retrieve_element_coordinate("Q5M1T1R")
result