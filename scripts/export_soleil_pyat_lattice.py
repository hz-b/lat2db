import json
import logging
import os
from itertools import zip_longest
from pathlib import Path
import at

from lat2db.tools.factories.pyat import factory
from lat2db.tools.pyat.compare_lattices import log_element_difference
from lat2db.tools.pyat.export_lattice_element_parameters import export_lattice_parameters, clear_left_over

logger = logging.getLogger("lat2db")
t_dir = Path(os.environ["SOLEIL_LAT_DIR"])


def check_load(filename: str, *, energy:float) -> at.Lattice:
    with open(filename, "rt") as fp:
        L = json.load(fp)
    return factory(dict(sequences=L), energy=energy)


def export_storage_ring(filename="soleil2_storage_ring_lattice.json"):
    src_filename = t_dir / "SOLEIL_II_V3631_sym1_V001_database.m"
    lat = at.load_m(src_filename)
    energy = lat.energy

    _, ring_props, _ = lat.get_optics()
    print(f"Soleil data as   imported {lat.cell_length} non integer tune {ring_props['tune']}")

    L = export_lattice_parameters(lat)

    L = [clear_left_over(elm) for elm in L]
    with open(filename, "wt") as fp:
        json.dump(L, fp, indent=2)

    lat
    r = check_load(filename, energy=energy)

    r = at.Lattice(r, energy=energy)
    elem_diff = [
        log_element_difference(a, b) for a, b, in zip_longest(lat, r) if not a.equals(b)
    ]
    _, ring_props, _ = r.get_optics()
    print(f"Soleil data as reimported {r.cell_length} non integer tune {ring_props['tune']}")
    print("Soleil\nElement Difference\n", "\n".join(elem_diff))


def main():
    export_storage_ring()


if __name__ == "__main__":
    main()
