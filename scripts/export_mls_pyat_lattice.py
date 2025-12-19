import json
import os
import pathlib
import sys
from itertools import zip_longest

import at

from lat2db.tools.factories.pyat import factory
from lat2db.tools.pyat.compare_lattices import (
    log_element_difference,
    plot_lattice_comparison,
)
from lat2db.tools.pyat.export_lattice_element_parameters import (
    export_lattice_parameters, clear_left_over,
)

path = pathlib.Path(os.environ["MLS_REFLAT"])
sys.path.insert(0, str(path / "storage_ring"))


def check_load(filename: str, *, energy: float) -> at.Lattice:
    with open(filename, "rt") as fp:
        L = json.load(fp)
    return factory(dict(sequences=L), energy=energy)


def export_storage_ring(filename="mls_storage_ring_reflat.json"):
    import mls_sr_reflat

    lat = mls_sr_reflat.mlsLattice()
    tmp = export_lattice_parameters(lat)
    tmp = [clear_left_over(elm) for elm in tmp]
    with open(filename, "wt") as fp:
        json.dump(tmp, fp, indent=4)

    energy = 0.629e9
    r = check_load(filename, energy=energy)
    # if cavity is off and no 6d tracking one can see a bit
    # of radiation difference
    r = at.Lattice(r, name="MLS chk", energy=energy)
    # r.enable_6d()
    # r.cavpts = "CAV*"
    # r.set_cavity_phase(cavpts=r.cavpts)

    elem_diff = [
        log_element_difference(a, b) for a, b, in zip_longest(lat, r) if not a.equals(b)
    ]

    elem_diff_txt ="\n".join(elem_diff)
    plot_lattice_comparison(lat, r, info_txt="MLS Storage Ring")
    print(f"""Brho diff{lat.BRho - r.BRho}
Element Difference
{elem_diff_txt}
""")

def main():
    export_storage_ring()

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    main()
    plt.show()
