import time
from pathlib import Path
from lark import Lark
from lat2db.bl.set_machine import create_machine
from lat2db.tools import dtclasses as ds
from lat2db.tools.madx.parser import MADXTransformer, parse


def export_elements(elements):
    """export elements as list"""

    def export_element(element_index, element):
        d = {key: val for key, val in element}
        d["index"] = element_index
        return d

    return [export_element(index, element) for index, element in enumerate(elements)]


default_version = ds.VersionInfo(major=0, minor=0, patch_level=0)
default_storage_format = ds.StorageFormatMetadata(
    version=ds.VersionInfo(major=0, minor=0, patch_level=0)
)


def export_lattice_properties(
        variables,
        *,
        machine_name,
        lattice_version=default_version,
        storage_format=default_storage_format
):
    physics = ds.LatticePhysicsProperties(
        ds.PhysicsParameter(name="energy", value=variables["energy"], egu="GeV")
    )
    geom = ds.LatticeGeometryProperties(is_ring=bool(variables["ringtype"]))
    smd = ds.LatticeMetadata(machine_name=machine_name, lattice_version=lattice_version,closed=True)
    return ds.Lattice(
        properties=ds.LatticeProperties(physics=physics, geometric=geom),
        storage_format=storage_format,
        lattice_standard_metadata=smd,
        user_meta_data={},
        timestamp=time.time(),
        elements=[],
    )


def export(organized_dict, variables):
    lp = export_lattice_properties(variables, machine_name="BESSYII")
    print("lppppp")
    print(lp)
    # lp.elements = export_elements(config.getAny("elements"))  # config
    lp.elements = list(organized_dict.values())

    try:
        create_machine(lp)
    except Exception as e:
        print(f"An exception occurred: {e}")

    return

    # d = dict(lattice_properties=lp, elements=element_configs)
    # json.dump(element_configs, sys.stdout, indent=4)


def main():
    BASE_DIR = Path(__file__).resolve().parent
    with (BASE_DIR / "b2_stduser_beamports_blm_tracy_corr.lat").open() as file: #add b2_stduser_beamports_blm_tracy_corr.lat in directory tools
        lattice_content = file.read()
    with (BASE_DIR / "madx.lark").open() as file:
        MADX_PARSER = Lark(file, parser="lalr", maybe_placeholders=True)
        file.seek(0)
    tree = MADX_PARSER.parse(lattice_content)
    machine_data = MADXTransformer().transform(tree)
    organized_dict = parse(machine_data)
    variables = machine_data['variables']
    export(organized_dict, variables)


if __name__ == "__main__":
    main()
