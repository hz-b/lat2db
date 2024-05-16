from lat2db.controller.get_machine_output import get_machine

machine = get_machine(machine_id="663223806d81d5e42b7f3746")
result = machine.retrieve_element_coordinate("Q5M1T1R")
result