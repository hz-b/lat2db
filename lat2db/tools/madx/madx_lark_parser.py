from .parser import MADXTransformer, parse
from importlib.resources import files
from lark import Lark

__all__ = ["get_madx_lark", "convert_madx_to_json"]



def get_madx_lark_file():
    return files(__name__.split(".")[0]).joinpath('tools/madx/madx.lark')

def get_madx_lark():
    with open(get_madx_lark_file(), "rt") as file:
        madx_parser = Lark(file, parser="lalr", maybe_placeholders=True)
        #: Todo: find out why that seek
        file.seek(0)
    return madx_parser

def convert_madx_to_json(lattice_content: str):
    tree = get_madx_lark().parse(lattice_content)
    machine_data = MADXTransformer().transform(tree)
    organized_dict = parse(machine_data)
    variables = machine_data['variables']

    return organized_dict, variables