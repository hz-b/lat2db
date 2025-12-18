"""
Todo:
    should I directly fill the data into the model here?

Currently it puts it in just basis types. Check can be made
by letting it instantiate at the end
"""

import functools
import logging
from typing import Dict, Any, Sequence, Tuple, Union

logger = logging.getLogger("lat2db")


def rename_parameter(
    inp: Dict[str, Any],
    parameters: Sequence[Tuple[str, str]],
    optional: bool = False,
    copy: bool = True,
) -> Dict[str, Any]:
    """ """
    if copy:
        inp = inp.copy()
    for src, tgt in parameters:
        if optional:
            val = inp.pop(src, None)
            if val is None:
                continue
        else:
            val = inp.pop(src)
        inp[tgt] = val
    return inp


def coeffs(inp: Dict[str, Sequence[float]]) -> Dict[str, Sequence[float]]:
    return dict(
        normal_cofficients=inp.pop("PolynomB"), skew_cofficients=inp.pop("PolynomA")
    )


def integration_parameters(inp: Dict[str, int]) -> Dict[str, int]:
    """
    Todo:
        unite with rework_integration as soon as passmethod is part
        of integration parameters
    """
    return dict(n_steps=int(inp.pop("NumIntSteps")), max_order=int(inp.pop("MaxOrder")))


def integration_method(inp: Dict[str, str]) -> Dict[str, str]:
    return dict(passmethod=inp.pop("PassMethod"))


def rework_main_magnet(
    inp: Dict[str, Union[str, int, float, Sequence[float]]],
    *,
    main_multipole: int,
    strength: float,
    copy: bool = True
) -> Dict[
    str, Union[
        str,
        int,
        float,
        Sequence[float],
        Dict[str, Sequence[float]],
        ]
    ]:
    if copy:
        inp = inp.copy()
    inp.update(**integration_method(inp))
    d = dict(
        magnetic_element=dict(
            coeffs=coeffs(inp),
            main_multipole_index=main_multipole,
            main_multipole_strength=strength,
            integration_parameters=integration_parameters(inp),
        )
    )
    #: todo: should the model be prepared that this data is not available ...
    kick_angles = inp.pop("KickAngle", [0.0, 0.0])
    d["kickangle"] = dict(x=kick_angles[0], y=kick_angles[1])

    inp["element_configuration"] = d
    return inp


def rework_sextupole(inp: Dict[str, Any], copy: bool = True) -> Dict[str, Any]:
    """
    Todo:
        should export corrector as an add on coil
    """
    if copy:
        inp = inp.copy()
    inp["tags"] = [inp.pop("Corrector")]
    inp = rework_main_magnet(inp, main_multipole=3, strength=inp.pop("H"))
    return inp


def rework_quadrupole(inp: Dict[str, Any], copy: bool = True) -> Dict[str, Any]:
    """
    Todo:
        should be prepared for piggy pack correctors
    """
    if copy:
        inp = inp.copy()
    inp["tags"] = []
    inp = rework_main_magnet(inp, main_multipole=2, strength=inp.pop("K"))
    return inp


def rework_dipole(inp: Dict[str, Any], copy: bool = True) -> Dict[str, Any]:
    if copy:
        inp = inp.copy()
    assert inp["type"] == "Bend"
    inp["type"] = "Dipole"
    val = inp.pop("Corrector", None)
    if val:
        inp["tags"] = [val]
    else:
        inp["tags"] = None
    inp = rename_parameter(
        inp,
        [
            ("BendingAngle", "bending_angle"),
            ("EntranceAngle", "entranceangle"),
            ("ExitAngle", "exitangle"),
            ("K", "gradient"),
        ],
    )
    inp = rename_parameter(
        inp,
        [
            ("FringeInt1", "fringeint1"),
            ("FringeInt2", "fringeint2"),
            ("FullGap", "fullgap"),
        ],
        optional=True,
    )
    inp = rework_main_magnet(inp, main_multipole=1, strength=None)
    return inp


def rework_drift(inp: Dict[str, Any], copy: bool = True) -> Dict[str, Any]:
    if copy:
        inp = inp.copy()
    inp.update(**integration_method(inp))
    return inp


def rework_marker(inp: Dict[str, Any], copy: bool = True) -> Dict[str, Any]:
    if copy:
        inp = inp.copy()
    inp.update(**integration_method(inp))
    return inp


def rework_monitor(inp: Dict[str, Any], copy: bool = True) -> Dict[str, Any]:
    if copy:
        inp = inp.copy()
    inp.update(**integration_method(inp))
    return inp


def rework_cavity(inp: Dict[str, Any], copy: bool = True) -> Dict[str, Any]:
    if copy:
        inp = inp.copy()
    inp["tags"] = []
    inp["harmonic_number"] = inp.pop("HarmNumber")
    inp["cavity_configuration"] = dict(
        frequency=inp.pop("Frequency"),
        voltage=inp.pop("Voltage"),
        energy=inp.pop("Energy"),
        timelag=inp.pop("TimeLag"),
    )
    inp.update(**integration_method(inp))
    return inp


refactory = dict(
    Monitor=rework_monitor,
    Marker=rework_marker,
    Drift=rework_drift,
    Sextupole=rework_sextupole,
    Quadrupole=rework_quadrupole,
    Bend=rework_dipole,
    RFCavity=rework_cavity,
)


@functools.lru_cache
def report_non_converted_element_type_once(t_type: str):
    logger.warning("No special conversion for element type %s", t_type)
    return type


def make_element_parameters_model_compliant(idx: int, elem: Dict[str, Any], copy: bool = True) -> Dict[str, Any]:
    """converts jsons  exported to lat2db data model
    """
    if copy:
        nelm = elem.copy()
    else:
        nelm = elem
    del elem

    cls = nelm.pop("Class")
    nelm["type"] = cls
    nelm["name"] = nelm.pop("FamName")
    nelm["length"] = nelm.pop("Length")
    nelm["index"] = idx

    # Why do some elements have a group info
    grp = nelm.pop("Group", None)
    if grp is not None:
        nelm["group"] = grp
    del grp

    f = refactory.get(cls, None)
    if f:
        nelm = f(nelm)
    else:
        report_non_converted_element_type_once(cls)

    return nelm


def export_lattice_parameters(lat: Sequence[object]) -> Sequence[Dict[str, Any]]:
    import jsons
    parameters = jsons.dump([elm.to_dict() for elm in lat])
    return [make_element_parameters_model_compliant(idx, elem) for idx, elem in enumerate(parameters)]


__all__ = []
