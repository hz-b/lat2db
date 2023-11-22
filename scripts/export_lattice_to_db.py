from tools.export_to_json import export

from pathlib import Path
from lark import Lark
from tools.parser import MADXTransformer, parse


def main():
    import os
    BASE_DIR = Path(__file__).resolve().parent.parent
    with (BASE_DIR / "tools/b2_stduser_beamports_blm_tracy_corr.lat").open() as file: #add b2_stduser_beamports_blm_tracy_corr.lat in directory tools
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
