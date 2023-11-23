from lat2db.tools.madx.madx_lark_parser import convert_madx_to_json
from lat2db.tools.export_to_json import export
from lat2db.tools.thor_scsi.thor_scsi_lark_parser import to_json
from pathlib import Path

def main(filename):
    with open(filename, "rt") as file:
       organized_dict, variables = convert_madx_to_json(file.read())
    # export(organized_dict, variables)

b2dir = t_dir = Path(__file__).resolve().parent / "lattice-files"  / "bessy2reflat" / "BESSYII"
if __name__ == "__main__":
    main(b2dir /  "BIIdesign" / "BESSYII_theory.madx")

if __name__ == "__main__":
    main(b2dir / "BIIstandarduser" / "BII_standarduserReference.seq")


if __name__ == "__main__":
    t_dir = Path(__file__).resolve().parent
    with open(t_dir / "b2_stduser_beamports_blm_tracy_corr.lat", "rt") as file:
       organized_dict, variables = to_json(file.read())


