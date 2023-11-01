from tools.export_to_json import export

from pathlib import Path
from lark import Lark
from tools.parser import MADXTransformer, parse


def main():
    import os

    home = os.environ["HOME"]
    #/home/schnizer/Devel/gitlab/dt4acc/lattices
    filename = os.path.join(
        home,
        "Devel", "gitlab",
        # "cpp", #name of the folder in your home directory where the thorscsi is. todo: move this to configuration instead of hardcoding
        "dt4acc",
        "lattices",
        "b2_stduser_beamports_blm_tracy_corr.lat", #name of the lattice file you want to read todo: move to configuration instead of hardcoding
    )

    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(filename, 'r') as file:
        lattice_content = file.read()
    with (BASE_DIR / "tools/madx.lark").open() as file:
        MADX_PARSER = Lark(file, parser="lalr", maybe_placeholders=True)
        file.seek(0)
    tree = MADX_PARSER.parse(lattice_content)
    machine_data = MADXTransformer().transform(tree)
    organized_dict = parse(machine_data)
    variables = machine_data['variables']
    export(organized_dict, variables)


if __name__ == "__main__":
    main()
