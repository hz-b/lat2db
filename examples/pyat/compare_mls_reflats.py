import sys

from lat2db.tools.pyat.mls_sr_reflat import mlsLattice

sys.path.append('/Users/safiullahomar/lattice/lat2db test')

from lat2db.tools.factories.pyat import factory
import json
import numpy as np
from pathlib import Path

import at
from bessy2_sr_reflat import bessy2Lattice
# Read json from file
t_dir = Path(__file__).resolve().parent
ring2 = mlsLattice()
bessyii_json_file = t_dir / "mls_lattice_json.json"
with open(bessyii_json_file, "rt") as fp:
    lattice_in_json_format = json.load(fp)

seq = factory(lattice_in_json_format[0])



ring = at.Lattice(seq,name='bessy2',periodicity=1, energy=629e6 )


file1_elements = ring  # List of elements from the first file
file2_elements = ring2  # List of elements from the second file

from collections import Counter

def elem_key(e):
    """Build a robust identity key for an element."""
    fam = getattr(e, 'FamName', None) or getattr(e, 'Name', None) or getattr(e, 'name', None)
    L = getattr(e, 'Length', None) if hasattr(e, 'Length') else getattr(e, 'L', None)
    cls = e.__class__.__name__
    # Key order chosen to be readable and stable
    return (fam, cls, L)

# Build a multiset (Counter) of ring1 element keys
ring1_counts = Counter(elem_key(e) for e in ring)

# Walk ring2; if an element's key isn't "consumed" from ring1_counts, it's extra in ring2
extra_in_ring2 = []
for idx, e in enumerate(ring2):
    k = elem_key(e)
    if ring1_counts[k] > 0:
        ring1_counts[k] -= 1   # consume a matching element from ring1 multiset
    else:
        # Not found (or too many occurrences in ring2) -> report it
        extra_in_ring2.append((idx, k))

# Pretty print
if extra_in_ring2:
    print("Elements present in ring2 but not in ring1 (by [FamName, Class, Length, PassMethod]):")
    for idx, (fam, cls, L) in extra_in_ring2:
        print(f"ring2 index {idx}: FamName={fam!r}, Class={cls}, Length={L}")
else:
    print("No extra elements in ring2 relative to ring1 (under the chosen identity key).")
