import sys

sys.path.append('/Users/safiullahomar/lattice/lat2db test')
from lat2db.tools.madx.madx_lark_parser import convert_madx_to_json
from lat2db.tools.export_to_json import export
from lat2db.tools.thor_scsi.thor_scsi_lark_parser import to_json
from pathlib import Path


def main(filename):
    print("another main")
    with open(filename, "rt") as file:
        #  organized_dict, variables = convert_madx_to_json(file.read())
        organized_dict, variables = to_json(file.read())

    export(organized_dict, variables)


if __name__ == "__main__":
    t_dir = Path(__file__).resolve().parent
    print("path os ", t_dir)
    file_path = t_dir / "b2_stduser_beamports_blm_tracy_corr.lat"
    main(file_path)
    """ with open(t_dir / "b2_stduser_beamports_blm_tracy_corr.lat", "rt") as file:
       organized_dict, variables = to_json(file.read()) """

""" 
if __name__ == "__main__":
   t_dir = Path(__file__).resolve().parent / "bessy2reflat" / "BESSYII" / "BIIstandarduser"
   main(t_dir / "BII_standarduserReference.seq") 
 """
