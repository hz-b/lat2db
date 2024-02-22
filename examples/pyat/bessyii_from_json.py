from lat2db.tools.factories.pyat import factory
import json
import numpy as np
from pathlib import Path

# Read json from file
t_dir = Path(__file__).resolve().parent
bessyii_json_file = t_dir / "bessyii_2_json_f44e7064-ba80-4f0c-a193-80997aa3d553.json"
with open(bessyii_json_file, "rt") as fp:
    lattice_in_json_format = json.load(fp)

seq = factory(lattice_in_json_format[0])


import at
ring = at.Lattice(seq,name='bessy2',periodicity=1, energy=1.7e9 )