from .parser import MADXTransformer, parse
from importlib.resources import files
from lark import Lark

__all__ = ["get_lark", "to_json"]



def get_lark_file():
    return files(__name__.split(".")[0]).joinpath('tools/thor_scsi/thor_scsi.lark')

def get_lark():
    with open(get_lark_file(), "rt") as file:
        parser = Lark(file, parser="lalr", maybe_placeholders=True)
        #: Todo: find out why that seek
        file.seek(0)
    return parser

def to_json(lattice_content: str):
    print("called to json")
    tree = get_lark().parse(lattice_content)
    machine_data = MADXTransformer().transform(tree)
    organized_dict = parse(machine_data)
    variables = machine_data['variables']
    return organized_dict, variables