import jsons

from lat2db.controller.get_at_ring_output import get_AT_ring_from_machine
from lat2db.controller.get_machine_output import get_machine_as_json
from lat2db.model.machine import Machine

class Accelerator:
    def __init__(self, uid: str):
        self.machine = get_machine_as_json(uid)
        self.ring = get_AT_ring_from_machine(self.machine)
        self.machine = jsons.load(self.machine, Machine)
