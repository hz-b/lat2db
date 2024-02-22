from lat2db.tools.factories.pyat import factory
import json
import numpy as np
from pathlib import Path
from bessy2_sr_reflat import bessy2Lattice
# Read json from file
t_dir = Path(__file__).resolve().parent
bessyii_json_file = t_dir / "bessyii_2_json_f44e7064-ba80-4f0c-a193-80997aa3d553.json"
with open(bessyii_json_file, "rt") as fp:
    lattice_in_json_format = json.load(fp)

seq = factory(lattice_in_json_format[0])


import at
ring = at.Lattice(seq,name='bessy2',periodicity=1, energy=1.7e9 )
ring2 = bessy2Lattice()

ring
ring2

file1_elements = ring  # List of elements from the first file
file2_elements = ring2  # List of elements from the second file

differences = []

for i in range(1188):  # Assuming 1188 elements in each file
    element1 = file1_elements[i]
    element2 = file2_elements[i]

    # Compare attributes of the elements
    if element1 != element2:
        differences.append((i, element1, element2))

if differences:
    print("Differences found:")
    for diff in differences:
        print(f"At index {diff[0]}: {diff[1]} != {diff[2]}")
else:
    print("No differences found. The Lattice files are identical.")