import json
import logging
import os
from pathlib import Path
from itertools import zip_longest

from lat2db.tools.factories.pyat import factory
from lat2db.tools.pyat.export_lattice_element_parameters import export_lattice_parameters, clear_left_over
from lat2db.tools.pyat.compare_lattices import (
    log_element_difference,
    plot_lattice_comparison,
)

import at

logger = logging.getLogger("lat2db")
t_dir = Path(os.environ["MAXIV_LAT_DIR"])


def check_load(filename: str, *, energy:float) -> at.Lattice:
    with open(filename, "rt") as fp:
        L = json.load(fp)
    return factory(dict(sequences=L), energy=energy)


def main(filename="max4_lattice.json"):
    if False:
        src_filename = t_dir / "from_any" / "max4_20121107_430e_AT2.m"
        lat = at.load_m(src_filename, energy=3.0e9)
    elif False:
        src_filename = t_dir / "from_any" / "not_to_share" / "max5_20120904_531_with_IDs_AT2.mat"
        lat = at.load_mat(src_filename)
    else:
        src_filename = t_dir / "R1.mat"
        lat = at.load_mat(src_filename)

    _, ring_props, _ = lat.get_optics()
    print(f"MAX V  data as imported {lat.cell_length} non integer tune {ring_props['tune']}")

    L = export_lattice_parameters(lat)

    L = [clear_left_over(elm) for elm in L]
    with open(filename, "wt") as fp:
        json.dump(L, fp, indent=4)

    energy=3e9
    r = check_load(filename, energy=energy)
    r = at.Lattice(r, energy=energy)
    elem_diff = [
        log_element_difference(a, b) for a, b, in zip_longest(lat, r) if not a.equals(b)
    ]

    _, ring_props, _ = r.get_optics()
    print(f"MAX V  data as imported {lat.cell_length} non integer tune {ring_props['tune']}")
    print("MAX IV\nElement Difference\n", "\n".join(elem_diff))



if __name__ == "__main__":
    main()