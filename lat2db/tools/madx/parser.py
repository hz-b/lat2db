import itertools
import math
from abc import ABC, abstractproperty
from dataclasses import dataclass

from lark import Transformer, v_args
@v_args(inline=True)
class AbstractLatticeFileTransformer(Transformer, ABC):
    REVERSED_SUFFIX = "_reversed"

    @abstractproperty
    def variables(self):
        pass

    def transform(self, tree):
        self.elements = {}
        self.lattices = {}
        self.commands = []
        super().transform(tree)
        return dict(
            elements=self.elements,
            lattices=self.lattices,
            commands=self.commands,
            variables=self.variables,
        )

    int = int
    float = float
    word = str
    name = lambda self, item: item.value.lower()
    string = lambda self, item: item[1:-1]

    def element(self, name, type_, *attributes):
        self.elements[name.lower()] = type_.lower(), dict(attributes)

    def attribute(self, name, value):
        return name.lower(), value

    def lattice(self, name, arangement):
        self.lattices[name.lower()] = list(arangement)

    def arrangement(self, multiplier, is_reversed, *items):
        multiplier = int(multiplier) if multiplier is not None else 1
        if is_reversed is not None:
            multiplier *= -1

        if multiplier < 0:
            items = items[::-1]

        return [x for _ in range(abs(multiplier)) for y in items for x in y]

    def ref_name(self, mutliplier, is_reversed, name):
        """

        Todo:
            review if name should be reversed
        """
        name = str(name).lower()
        multiplier = int(mutliplier) if mutliplier is not None else 1
        if is_reversed is not None:
            multiplier *= -1

        if multiplier < 0:
            name = self.reverse_object(name)

        return abs(multiplier) * (name,)

    def reverse_object(self, name):
        if name.endswith(self.REVERSED_SUFFIX):
            reversed_name = name[: -len(self.REVERSED_SUFFIX)]
        else:
            reversed_name = name + self.REVERSED_SUFFIX
        if reversed_name in self.lattices or reversed_name in self.elements:
            pass
        elif name in self.lattices:
            self.lattices[reversed_name] = [
                self.reverse_object(obj_name)
                for obj_name in reversed(self.lattices[name])
            ]
        elif name in self.elements:
            # a bend with different exit and entrance angles must be reversed
            # for all other elements we can return the old reference
            # TODO: must other elemetns be reversed too?
            type_, attrs = self.elements[name]
            if type_ not in {"sbend", "csbend"} or attrs.get("e1") == attrs.get("e2"):
                return name

            attrs = attrs.copy()
            attrs["e1"], attrs["e2"] = attrs["e2"], attrs["e1"]
            self.elements[reversed_name] = type_, attrs
        return reversed_name


@v_args(inline=True)
class ArithmeticTransformer(Transformer):
    def __init__(self, variables=None):
        if variables is None:
            self._variables = {"pi": math.pi, "twopi": 2 * math.pi, "e": math.e}
        else:
            self._variables = variables

    @property
    def variables(self):
        return self._variables

    identity = lambda self, object: object
    number = float
    word = str
    from operator import add, sub, mul, truediv as div, neg, pow

    def assignment(self, name, value):
        self.variables[name.lower()] = value
        return value

    def function(self, function, operand):
        # some math functions are named differently in Python
        function = {"arctan": "atan"}.get(function, function)
        return getattr(math, function.lower())(operand)

    def variable(self, name):
        try:
            return self.variables[name.lower()]
        except KeyError:
            # There is no syntactic distinction between a variable and a string.
            # The best thing we can do is to test if it is a variable or not.
            return name
            # raise UndefinedVariableError(name)

@dataclass(frozen=True)
class MADXSequenceEntryAtPosition:
    #: actually an identifier
    name : str
    #: posiiton it is placed at
    pos : float

@v_args(inline=True)
class MADXTransformer(ArithmeticTransformer, AbstractLatticeFileTransformer):
    def sequence(self, name, *items):
        """
        Todo:
            get rid of lowering name
        """
        *attributes, elements = items
        self.lattices[name.lower()] = elements
        self.commands.append(("name", name))

    def seq_element(self, name, value):
        """
        Todo:
            get rid of lowering name
        """
        return MADXSequenceEntryAtPosition(name=name.lower(), pos=value)

    def seq_elements(self, *elements):
        return list(elements)



def parse(machine_data):
    """combine information from different places to a single one
    """
    # Iterate through elements and create a new dictionary
    organised_dict = {}
    index_iter = itertools.count()

    # see if expected entries are there
    lattice_data = machine_data['lattices']
    element_data = machine_data['elements']


    def parse_sublattice(sub_lattice, *, contained_within):
        for entry in sub_lattice:
            # find out if it is a sub lattice:
            is_element = True
            try:
                sub_sub_lat = lattice_data[entry]
                is_element = False
                parse_sublattice(sub_sub_lat, contained_within=contained_within.copy() + [entry])
            except KeyError as exc:
                # todo: limit exception
                pass

            if is_element:
                # here no identities anymore: "complexity hourray"
                # a salute to some miss
                if isinstance(entry, MADXSequenceEntryAtPosition):
                    pos_name = entry.name
                    pos_val = float(entry.pos)
                else:
                    pos_name = entry
                    pos_val = None
                # how to check compliance
                pos_name = str(pos_name)
                element_type, values = machine_data['elements'][pos_name]
                element_type = element_type.capitalize()
                organised_dict[next(index_iter)] = dict(type=element_type, name=pos_name, at_pos=pos_val, contained_within=contained_within, **values)

    parse_sublattice(machine_data['lattices']['ring'], contained_within=[])
        # now resolve the type
    return organised_dict