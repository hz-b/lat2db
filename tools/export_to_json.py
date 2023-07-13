import json
import sys
import time

from thor_scsi.factory import accelerator_from_config, parse_config_file

from src.bl.set_machine import create_machine
# import

from tools import dtclasses as ds


def export_elements(elements):
    """export elements as list"""
    def export_element(element_index, element):
        d= {key: val for key, val in element}
        d["index"] = element_index
        return d

    return [export_element(index, element) for index, element in enumerate(elements)]


default_version = ds.VersionInfo(major=0, minor=0, patch_level=0)
default_storage_format = ds.StorageFormatMetadata(
    version=ds.VersionInfo(major=0, minor=0, patch_level=0)
)


def export_lattice_properties(
    config,
    *,
    machine_name,
    lattice_version=default_version,
    storage_format=default_storage_format
):
    physics = ds.LatticePhysicsProperties(
        ds.PhysicsParameter(name="energy", value=config.getAny("Energy"), egu="GeV")
    )
    geom = ds.LatticeGeometryProperties(is_ring=bool(config.getAny("ringtype")))
    smd = ds.LatticeMetadata(machine_name=machine_name, lattice_version=lattice_version)
    return ds.Lattice(
        properties=ds.LatticeProperties(physics=physics, geometric=geom),
        storage_format=storage_format,
        lattice_standard_metadata=smd,
        user_meta_data={},
        timestamp=time.time(),
        elements=[],
    )


def export(config):
    lp = export_lattice_properties(config, machine_name="BESSYII")
    lp.elements = export_elements(config.getAny("elements"))
    create_machine(lp)
    return

    d = dict(lattice_properties=lp, elements=element_configs)
    json.dump(element_configs, sys.stdout, indent=4)


def main():
    import os

    home = os.environ["HOME"]
    filename = os.path.join(
        home,
        "cpp", #name of the folder in your home directory where the thorscsi is. todo: move this to configuration instead of hardcoding
        "dt4acc",
        "lattices",
        "b2_stduser_beamports_blm_tracy_corr.lat", #name of the lattice file you want to read todo: move to configuration instead of hardcoding
    )

    lat = accelerator_from_config(filename)
    config = parse_config_file(filename)
    export(config)


if __name__ == "__main__":
    main()
