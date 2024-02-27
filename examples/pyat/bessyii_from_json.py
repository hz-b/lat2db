import sys

from lat2db.tools.factories.pyat import factory
import json
import numpy as np
from pathlib import Path

import at
from bessy2_sr_reflat import bessy2Lattice
# Read json from file
t_dir = Path(__file__).resolve().parent
bessyii_json_file = t_dir / "bessyii_lattice_json.json"
with open(bessyii_json_file, "rt") as fp:
    lattice_in_json_format = json.load(fp)

seq = factory(lattice_in_json_format[0])



ring = at.Lattice(seq,name='bessy2',periodicity=1, energy=1.7e9 )
ring2 = bessy2Lattice()

# twiss = ring.get_optics(at.All)
ring
ring2

file1_elements = ring  # List of elements from the first file
file2_elements = ring2  # List of elements from the second file

differences = []
for i in range(1188):  # Assuming 1188 elements in each file
    element1 = file1_elements[i]
    element2 = file2_elements[i]

    # Get all field names for each element as sets
    element1_fields = set(vars(element1).keys())
    element2_fields = set(vars(element2).keys())

    # Compare fields present in element1 but not in element2
    for field in element1_fields - element2_fields:
        differences.append((i, field, getattr(element1, field), None))

    # Compare fields present in element2 but not in element1
    for field in element2_fields - element1_fields:
        differences.append((i, field, None, getattr(element2, field)))

    # Compare common fields
    for field in element1_fields.intersection(element2_fields):
        value1 = getattr(element1, field)
        value2 = getattr(element2, field)

        if isinstance(value1, np.ndarray) and isinstance(value2, np.ndarray):
            # Compare arrays element-wise
            if not np.array_equal(value1, value2):
                differences.append((i, field, value1, value2))
        elif value1 != value2:
            differences.append((i, field, value1, value2))

if differences:
    print("Differences found:")
    for diff in differences:
        index = diff[0]
        field_name = diff[1]
        value1 = diff[2]
        value2 = diff[3]
        if value1 is None:
            print(f"At index {index}: '{field_name}' is in AT but not in BESSY")
        elif value2 is None:
            pass
            # print(f"At index {index}: '{field_name}' is in AT but not in BESSYII")
        else:
            if field_name == "PolynomB":
                chk1 = np.array(value1, dtype=float)
                chk2 = np.array(value2, dtype=float)
                diff = chk1 - chk2
                if (np.absolute(diff) > 1e-6).any():
                    print(f"At index  {index}: '{field_name}' differs: {chk1} != {chk2}")
            else:
                print(f"At index {index}: '{field_name}' differs: {value1} != {value2}")
else:
    print("No differences found. The Lattice files are identical.")