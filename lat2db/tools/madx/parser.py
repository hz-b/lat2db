
import math
from abc import ABC, abstractproperty
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
        name = str(name).lower()
        multiplier = int(mutliplier) if mutliplier is not None else 1
        if is_reversed is not None:
            multiplier *= -1

        if multiplier < 0:
            name = self.reverse_object(name)

        return abs(multiplier) * (name,)


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


@v_args(inline=True)
class MADXTransformer(ArithmeticTransformer, AbstractLatticeFileTransformer):
    def sequence(self, name, *items):
        *attributes, elements = items
        self.lattices[name.lower()] = elements
        self.commands.append(("name", name))

    def seq_element(self, name, value):
        return name.lower(), value

    def seq_elements(self, *elements):
        return list(elements)


def parse(machine_data):
    """combine information from different places to a single one
    """
    # Iterate through elements and create a new dictionary
    organised_dict = {}

    index = -1
    for pos_name, pos_val in machine_data['lattices']['ring']:
        index += 1
        element_type, values = machine_data['elements'][pos_name]
        element_type = element_type.capitalize()
        organised_dict[index] = dict(type=element_type, name=pos_name, at_pos=pos_val, **values)
        # now resolve the type
    return organised_dict