import at

from lat2db.model.machine import Machine
from lat2db.tools.factories.pyat import factory


def get_AT_ring_from_machine(machine : Machine, *, energy):
    """
    Todo:
        eneregy should be part of config
    """
    seq = factory(machine, energy)

    ring = at.Lattice(seq, name='bessy2', periodicity=1, energy=energy)

    if machine['closed']:
        # need to add this info in diff
        ring.enable_6d()
        # Set main cavity phases
        ring.set_cavity_phase(cavpts='CAV*')
    return ring