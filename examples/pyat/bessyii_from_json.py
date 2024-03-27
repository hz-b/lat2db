import json
from pathlib import Path

import at
from lat2db.tools.factories.pyat import factory

# Read json from file
t_dir = Path(__file__).resolve().parent
bessyii_json_file = t_dir / "bessyii_lattice_json.json"
with open(bessyii_json_file, "rt") as fp:
    lattice_in_json_format = json.load(fp)

seq = factory(lattice_in_json_format[0])

ring = at.Lattice(seq, name='bessy2', periodicity=1, energy=1.7e9)
if True:
    # set up of calculation choice
    ring.enable_6d()  # Should 6D be default?
    # Set main cavity phases
    ring.set_cavity_phase(cavpts='CAV*')
orbit = ring.find_orbit(at.All)
twiss = ring.get_optics(at.All)
