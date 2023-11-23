
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
    # Iterate through elements and create a new dictionary
    new_dict = {}
    for key, (element_type, element_values) in machine_data['elements'].items():
        # Capitalize the first letter of element_type
        element_type = element_type.capitalize()

        # Capitalize the first letter of keys and values in element_values dictionary
        formatted_element_values = {k.capitalize(): v for k, v in element_values.items()}

        new_dict[key] = {
            'name': key,
            'type': element_type,
            **formatted_element_values  # Flatten element_values dictionary
        }
        # Extract the ring sequence
        ring_sequence = machine_data['lattices']['ring']

        # Create a new dictionary based on the ring sequence
        organized_dict = {}
        index = 0
        for key in ring_sequence:
            if key == 'start':
                organized_dict[index] = {'index': index, 'name': 'start', 'type': 'Marker'}
                index += 1
            elif key == 'ringend':
                organized_dict[index] = {'index': index, 'name': 'ringend', 'type': 'Marker'}
                index += 1
            else:
                # expand key: e.g. if sublattice
                for item in machine_data['lattices'][key]:
                    if item in new_dict:
                        organized_dict[index] = {**new_dict[item], 'index': index}
                        index += 1
    return organized_dict