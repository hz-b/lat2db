import logging
import numpy as np

logger = logging.getLogger("lat2db")


class LioninCario:
    """A class not defined anywhere

    The name: how does a software engineer search a lion in Africa?
    """

    def __str__(self):
        return "LioninCairo(not defined)"


a_lion = LioninCario()


def t_cmp(va, vb) -> bool:
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
    assert flag is not None
    return flag


def log_element_difference(a, b) -> str:
    flag = a.equals(b)
    assert not flag, f"Unexpected {a} matches {b}"

    chk = a != b
    da = a.to_dict()
    db = b.to_dict()
    keys = list(da) + list(db)

    def h(k):
        return t_cmp(da.get(k, a_lion), db.get(k, a_lion))

    diff_prop = [
        f"{k}: a={da.get(k, a_lion)}, b={db.get(k, a_lion)}" for k in keys if not h(k)
    ]
    return f"{a.FamName:20s}: a != b. {chk=} ; differ in {diff_prop}"


class OffsetFromRegressionLine:
    def __init__(self):
        self.slope = None
        self.intercept = None

    def create_reference_fit(self, indep, dep):
        self.slope, self.intercept = np.polyfit(indep, dep, 1)
        logger.warning(
            f"{self.__class__.__name__}: reference a={self.intercept} b={self.slope}"
        )

    def __call__(self, indep, dep):
        if self.slope is None:
            assert self.intercept is None
            self.create_reference_fit(indep, dep)

        ref = self.intercept + self.slope * np.asarray(indep)
        return np.asarray(dep) - ref


def plot_lattice_comparison(a, b, *, info_txt: str):
    """plot betafunction and tune using at to calculate it"""
    import matplotlib.pyplot as plt
    import at

    a = a
    _, ring_props, twiss = a.get_optics(at.All)
    print(
        f"{info_txt} version a:  {a.cell_length} non integer tune {ring_props['tune']}"
    )

    lft_ax, rght_ax, synopt_ax = at.plot_beta(a)
    for lines in lft_ax.get_lines() + rght_ax.get_lines():
        lines.set_linestyle("--")

    s = a.get_s_pos()
    pmu = twiss["mu"] / (2 * np.pi)
    fig, (ax_tune_x, ax_tune_y) = plt.subplots(2, 1, sharex=True)
    ax_tune_x.plot(s, pmu[:, 0])
    ax_tune_x.set_ylabel(r"$\mu_x$")
    ax_tune_y.plot(s, pmu[:, 1])
    ax_tune_y.set_ylabel(r"$\mu_y$")

    fig, (ax_tune_ox, ax_tune_oy) = plt.subplots(2, 1, sharex=True)
    off_x = OffsetFromRegressionLine()
    off_y = OffsetFromRegressionLine()
    ax_tune_ox.plot(s, off_x(s, pmu[:, 0]))
    ax_tune_ox.set_ylabel(r"$\mu_x - |\mu_x|$")
    ax_tune_oy.plot(s, off_y(s, pmu[:, 1]))
    ax_tune_oy.set_ylabel(r"$\mu_y - |\mu_y|$")

    b = b
    at.plot_beta(b, axes=(lft_ax, rght_ax))
    _, ring_props, chk_twiss = b.get_optics(at.All)

    chk_pmu = chk_twiss["mu"] / (2 * np.pi)
    ax_tune_x.plot(s, chk_pmu[:, 0], ".--", label="x")
    ax_tune_y.plot(s, chk_pmu[:, 1], ".--", label="y")

    ax_tune_ox.plot(s, off_x(s, chk_pmu[:, 0]), ".--", label="x")
    ax_tune_oy.plot(s, off_y(s, chk_pmu[:, 1]), ".--", label="y")

    fig, (ax_tune_dx, ax_tune_dy) = plt.subplots(2, 1, sharex=True)
    ax_tune_dx.plot(s, chk_pmu[:, 0] - pmu[:, 0], ".-")
    ax_tune_dx.set_ylabel(r"${\mu_x}_a - {\mu_x}_b$")
    ax_tune_dy.plot(s, chk_pmu[:, 1] - pmu[:, 1], ".-")
    ax_tune_dy.set_ylabel(r"${\mu_y}_a - {\mu_y}_b$")

    for ax in ax_tune_y, ax_tune_dy, ax_tune_oy:
        ax.set_xlabel("s [m]")
    for ax in ax_tune_x, ax_tune_dx, ax_tune_ox:
        ax.set_title(info_txt)

    opt_at_elem_0, ring_props, twiss = at.get_optics(b, refpts=[0, len(b) - 1])
    print(f" {b.cell_length}")
    print(
        f"{info_txt} version b:  {b.cell_length} non integer tune {ring_props['tune']}"
    )


__all__ = ["log_element_difference", "plot_lattice_comparison"]
