import json

from lat2db.tools.factories.pyat import factory
from pathlib import Path

# Read json from file
t_dir = Path(__name__).resolve().parent
bessyii_json_file = t_dir / "bessyii_json_f44e7064-ba80-4f0c-a193-80997aa3d553.json"
with open(bessyii_json_file, "rt") as fp:
    lattice_in_json_format = json.load(fp)

seq = factory(lattice_in_json_format)


import at
acc = at.Lattice(seq)