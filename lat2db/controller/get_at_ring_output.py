import at

from lat2db.model.machine import Machine
from lat2db.tools.factories.pyat import factory


def get_AT_ring_from_machine(machine : Machine):
    seq = factory(machine)

    ring = at.Lattice(seq, name='bessy2', periodicity=1, energy=1.7e9)
    ring.enable_6d()  # Should 6D be default?
    # Set main cavity phases
    if machine['closed']:
        ring.set_cavity_phase(cavpts='CAV*')
    return ring