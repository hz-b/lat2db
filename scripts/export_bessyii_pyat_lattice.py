"""Export BESSY II lattice as pure json

Reads it back in to check that it complies to the model
"""
import os
import sys
import pathlib

import json
from itertools import zip_longest

import at
import numpy as np

from lat2db.model.element import Element
from lat2db.tools.factories.pyat import factory, logger
from lat2db.tools.pyat.export_lattice_element_parameters import export_lattice_parameters
import matplotlib.pyplot as plt

path = pathlib.Path(os.environ["BESSYII_REFLAT"])
sys.path.insert(0, str(path / "injection_line"))
sys.path.insert(0, str(path / "booster"))
sys.path.insert(0, str(path / "storage_ring"))


def compare_element_basis(a: at.Element, b: at.Element):
    assert a.FamName == b.FamName
    assert a.Length == b.Length
    assert a.PassMethod == b.PassMethod


def noop(a: at.Element, b: at.Element):
    pass

def compare_drift(a: at.Drift, b: at.Drift):
    pass

def compare_magnet_parameters(a: at.Multipole, b: at.Multipole):
    assert np.asarray(a.KickAngle) == np.asarray(b.KickAngle)

def compare_sextupole(a: at.Sextupole, b: at.Sextupole):
    pass

compare_factory=dict(
    Monitor=noop,
    Marker=noop,
    Drift=noop,
    Quadrupole=noop,
    Sextupole=compare_sextupole,
    Dipole=noop,
    RFCavity=noop,
)

def compare_position(a: at.Element, b: at.Element):
    assert a.dx == b.dx
    assert a.dy == b.dy
    assert a.dy == b.dz
    assert a.tilt == b.tilt


def t_cmp(va, vb):
    if va is a_lion or vb is a_lion:
        # key was not available in one of the dictionaries
        return False
    flag = None
    try:
        flag = np.allclose(va, vb, atol=1e-12, rtol=1e-12)
    except TypeError:
        pass

    if flag is None:
        flag = va == vb
        return flag

    if isinstance(flag, np.ndarray):
        flag = flag.all()
    assert flag  is not None
    return flag

    return

class LioninCario:
    def __str__(self):
        return "LioninCairo(not defined)"

a_lion = LioninCario()

def compare_element(a: at.Element, b: at.Element):
    compare_element_basis(a, b)
    compare_position(a, b)
    flag = a.equals(b)
    if not flag:
        chk = a != b
        da = a.to_dict()
        db = b.to_dict()
        keys = list(da) + list(db)
        def h(k):
            return t_cmp(da.get(k, a_lion), db.get(k, a_lion))

        diff_prop = [f"{k}: a={da.get(k, a_lion)}, b={db.get(k, a_lion)}" for k in keys if not h(k)]
        print(f"{a.FamName:20s}: a != b. {chk=} ; differ in {diff_prop}")

    f = compare_factory[a.__class__.__name__]
    return f(a, b)


def check_load(filename: str) -> at.Lattice:
    with open(filename, "rt") as fp:
        L = json.load(fp)
    return factory(dict(sequences=L), energy=1.75e9)


class OffsetFromRegressionLine:
    def __init__(self):
        self.slope = None
        self.intercept = None

    def create_reference_fit(self, indep, dep):
        self.slope, self.intercept = np.polyfit(indep, dep, 1)
        logger.warning(f"{self.__class__.__name__}: reference a={self.intercept} b={self.slope}")

    def __call__(self, indep, dep):
        if self.slope is None:
            assert self.intercept is None
            self.create_reference_fit(indep, dep)

        ref = self.intercept + self.slope * np.asarray(indep)
        return np.asarray(dep) - ref


def export_storage_ring(filename="bessy2_storage_ring_reflat.json"):
    import bessy2_sr_reflat

    lat = bessy2_sr_reflat.bessy2Lattice()
    _, ring_props, twiss = lat.get_optics(at.Allxelpy   _length} non integer tune {ring_props['tune']}")

    lft_ax, rght_ax, synopt_ax = at.plot_beta(lat)
    for lines in lft_ax.get_lines() + rght_ax.get_lines():
        lines.set_linestyle('--')
    # at.plot_linear(lat)

    s = lat.get_s_pos()
    pmu = twiss["mu"] / (2 * np.pi)
    fig, (ax_tune_x, ax_tune_y) = plt.subplots(2, 1, sharex=True)
    ax_tune_x.plot(s, pmu[:, 0])
    ax_tune_x.set_ylabel(r"$\mu_x$")
    ax_tune_y.plot(s, pmu[:, 1])
    ax_tune_y.set_ylabel(r"$\mu_x$")

    fig, (ax_tune_ox, ax_tune_oy) = plt.subplots(2, 1, sharex=True)
    off_x = OffsetFromRegressionLine()
    off_y = OffsetFromRegressionLine()
    ax_tune_ox.plot(s, off_x(s, pmu[:, 0]))
    ax_tune_ox.set_ylabel(r"$\mu_x - |\mu_x|$")
    ax_tune_oy.plot(s, off_y(s, pmu[:, 1]))
    ax_tune_oy.set_ylabel(r"$\mu_y - |\mu_y|$")
    tmp = export_lattice_parameters(lat)


    with open(filename, "wt") as fp:
        json.dump(tmp, fp, indent=4)

    r = check_load(filename)
    energy = 1.7185e9
    r = at.Lattice(r, name="BESSY II chk", energy=energy)
    r.enable_6d()
    r.cavpts = "CAV*"
    r.set_cavity_phase(cavpts=r.cavpts)

    [compare_element(a, b) for a, b, in zip_longest(lat, r)]

    print("Brho diff:", lat.BRho - r.BRho)
    at.plot_beta(r, axes=(lft_ax, rght_ax))
    _, ring_props, chk_twiss = r.get_optics(at.All)

    chk_pmu = chk_twiss["mu"] / (2 * np.pi)
    ax_tune_x.plot(s,chk_pmu[:, 0], '.--', label="x")
    ax_tune_y.plot(s,chk_pmu[:, 1], '.--', label="y")

    ax_tune_ox.plot(s,off_x(s, chk_pmu[:, 0]), '.--', label="x")
    ax_tune_oy.plot(s,off_y(s, chk_pmu[:, 1]), '.--', label="y")

    fig, (ax_tune_dx, ax_tune_dy) = plt.subplots(2, 1, sharex=True)
    ax_tune_dx.plot(s, chk_pmu[:,0] - pmu[:,0], '.-')
    at.plot_synopt(r, axes=ax_tune_dy)
    ax_tune_dy.plot(s, chk_pmu[:,1] - pmu[:,1], '.-')

    print(f"BESSY II data as reimported {r.cell_length} non integer tune {ring_props['tune']}")

    opt_at_elem_0, ring_props, twiss= at.get_optics(r, refpts=[0, len(r)-1])
    print(f"BESSY II {r.cell_length}")


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
    main()
    plt.show()