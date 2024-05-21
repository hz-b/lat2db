from lat2db.controller.get_at_ring_output import get_AT_ring_from_machine
from lat2db.controller.get_machine_output import get_machine_as_json, get_machine_as_json_from_db
from lat2db.model.machine import Machine


class Accelerator:
    def __init__(self, uid: str = None, file_name: str = None, from_json: bool = False):
        if from_json:
            result = get_machine_as_json(file_name)
            if isinstance(result, list):
                self.machine = result[0]
            else:
                self.machine = result
        else:
            self.machine = get_machine_as_json_from_db(uid)
        self.ring = get_AT_ring_from_machine(self.machine)
        self.machine = Machine(**self.machine)
