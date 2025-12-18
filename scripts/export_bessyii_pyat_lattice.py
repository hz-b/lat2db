"""Export BESSY II lattice as pure json

Reads it back in to check that it complies to the model
"""
import os
import sys
import pathlib

import json
from itertools import zip_longest

import at

from lat2db.tools.factories.pyat import factory
from lat2db.tools.pyat.compare_lattices import log_element_difference, OffsetFromRegressionLine, plot_lattice_comparison
from lat2db.tools.pyat.export_lattice_element_parameters import export_lattice_parameters

path = pathlib.Path(os.environ["BESSYII_REFLAT"])
sys.path.insert(0, str(path / "injection_line"))
sys.path.insert(0, str(path / "booster"))
sys.path.insert(0, str(path / "storage_ring"))


def check_load(filename: str) -> at.Lattice:
    with open(filename, "rt") as fp:
        L = json.load(fp)
    return factory(dict(sequences=L), energy=1.75e9)


def export_storage_ring(filename="bessy2_storage_ring_reflat.json"):
    import bessy2_sr_reflat

    lat = bessy2_sr_reflat.bessy2Lattice()
    tmp = export_lattice_parameters(lat)

    with open(filename, "wt") as fp:
        json.dump(tmp, fp, indent=4)

    r = check_load(filename)
    energy = 1.7185e9
    r = at.Lattice(r, name="BESSY II chk", energy=energy)
    r.enable_6d()
    r.cavpts = "CAV*"
    r.set_cavity_phase(cavpts=r.cavpts)

    elem_diff = [log_element_difference(a, b) for a, b, in zip_longest(lat, r) if not a.equals(b)]

    plot_lattice_comparison(lat, r, info_txt="BESSY II Storage Ring")
    print("Brho diff:", lat.BRho - r.BRho)
    print("Element Difference", "\n".join(elem_diff))




def export_booster(filename="bessy2_booster_reflat.json"):
    import bessy2_booster_reflat

    lat = bessy2_booster_reflat.bessy2Booster()
    tmp = export_lattice_parameters(lat)
    with open(filename, "wt") as fp:
        json.dump(tmp, fp, indent=4)

    check_load(filename)


def export_injection_line(filename="bessy2_injection_line_reflat.json"):
    import bessy2_IL_reflat

    lat = bessy2_IL_reflat.bessy2_IL()
    tmp = export_lattice_parameters(lat)
    with open(filename, "wt") as fp:
        json.dump(tmp, fp, indent=4)

    check_load(filename)


def main():
    export_storage_ring()
    export_booster()
    export_injection_line()


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    main()
    plt.show()