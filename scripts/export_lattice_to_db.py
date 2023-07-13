from tools.export_to_json import export

from thor_scsi.factory import parse_config_file

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

    config = parse_config_file(filename)
    export(config)


if __name__ == "__main__":
    main()
