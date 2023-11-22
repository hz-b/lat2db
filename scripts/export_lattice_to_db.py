from lat2db.tools.madx_lark_parser import convert_madx_to_json
from lat2db.tools.export_to_json import export
from pathlib import Path

def main():
    # BASE_DIR = Path(__file__).resolve().parent.parent
    # with (BASE_DIR / "tools/b2_stduser_beamports_blm_tracy_corr.lat").open() as file: #add b2_stduser_beamports_blm_tracy_corr.lat in directory tools
    #     lattice_content = file.read()

    t_dir = Path(__file__).resolve().parent
    with open(t_dir / "b2_stduser_beamports_blm_tracy_corr.lat") as file:
       organized_dict, variables = convert_madx_to_json(file.read())
    export(organized_dict, variables)


if __name__ == "__main__":
    main()
