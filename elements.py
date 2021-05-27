"""
elements.py

A module containing implementaions of logic elements.
You can use the following classes from this module:
- Connnection
- Constant
- AndGate
- OrGate
- NotGate
- XorGate
- NandGate
- NorGate
"""


import functools


class Connection:
    """Represents the connection between the output of some element with the input of
    another element.

    Attributes
    ----------
    source: BasicElement
        the logic element from which binary output is taken
    output_label: str
        the name of the output of the source element (it can have several outputs)
    destination: BasicElement
        the logic element, to which the signal is passed
    input_label: str
        the name of the input of the destination element (it can have several inputs)
    """
    def __init__(self, source, output_label, destination, input_label):
        self._source = source
        self._output_label = output_label
        self._destination = destination
        self._input_label = input_label

    @property
    def source(self):
        return self._source

    @property
    def output_label(self):
        return self._output_label

    @property
    def destination(self):
        return self._destination

    @property
    def input_label(self):
        return self._input_label


class BasicElement:
    """An abstract class for defining the interface of logic elements.

    Logic element:
    - has inputs with associated labels
    - each input is associated with zero or one connections (see class Connection)
    - has outputs with associated labels
    - each output can be associated with any number of connections (see class Connection).

    Attributes
    ----------
    value: tuple
        return the tuple of booleans (one boolean for one output of the element)

    Methods
    -------
    set_input_connection(input_label, connection)
        Associate the passed in connection with the specified input
    delete_input_connection(input_label)
        Delete the connection associated with the specified input
    set_output_connection(input_label, connection)
        Add passed in connection to the connections associated with the specified input
    delete_output_connection(input_label, connection)
        Clear all the connections
    reset_value()
        Forgets the previously calculated value
    """
    def __init__(self):
        self._ins = {}
        self._outs = {}
        self._value = None

    def set_input_connection(self, input_label: str, connection: Connection):
        self._ins[input_label] = connection

    def delete_input_connection(self, input_label: str):
        self._ins[input_label] = None

    def set_output_connection(self, output_label: str, connection: Connection):
        self._outs[output_label].append(connection)

    def delete_output_connection(self, output_label: str):
        self._outs[output_label] = []

    @property
    def value(self):
        raise NotImplementedError

    def reset_value(self):
        pass


class BasicLogicGate(BasicElement):
    """An abstract class for basic logic gates (such as AND, OR, NOT, XOR, NAND, NOR).
    AndGate, OrGate, XorGate, NandGate and NorGate classes inherit from this class.

    This class provides multi-input variants of the elements mentioned above.
    """

    def __init__(self, num_inputs: int):
        """Initialize an instance with num_inputs.
        :num_inputs: the number of inputs of an element
        """
        if num_inputs < 2:
            raise ValueError("Number of inputs should be >= 2")
        super().__init__()
        self._num_inputs = num_inputs
        for i in range(1, num_inputs+1):
            self._ins['in' + str(i)] = None
        self._outs['out'] = []

    def _logic_of_element(self, *inputs) -> bool:
        raise NotImplementedError

    def _iterate_over_input_values(self):
        for input_label in self._ins:
            if self._ins[input_label] is None:
                yield False
            else:
                yield self._ins[input_label].source.value

    @property
    def value(self):
        if self._value is None:
            self._value = self._logic_of_element(*self._iterate_over_input_values())
        return self._value

    def reset_value(self):
        self._value = None


class AndGate(BasicLogicGate):
    def _logic_of_element(self, *inputs):
        return functools.reduce(lambda a, b: a and b, inputs)

class OrGate(BasicLogicGate):
    def _logic_of_element(self, *inputs):
        return functools.reduce(lambda a, b: a or b, inputs)

class XorGate(BasicLogicGate):
    def _logic_of_element(self, *inputs):
        return functools.reduce(lambda a, b: a != b, inputs)

class NandGate(BasicLogicGate):
    def _logic_of_element(self, *inputs):
        return not functools.reduce(lambda a, b: a and b, inputs)

class NorGate(BasicLogicGate):
    def _logic_of_element(self, *inputs):
        return not functools.reduce(lambda a, b: a or b, inputs)

class NotGate(BasicElement):
    def __init__(self):
        super().__init__()
        self._ins['in'] = None
        self._outs['out'] = []

    @property
    def value(self):
        if self._value is None:
            if self._ins['in'] is None:
                in_ = False
            else:
                in_ = self._ins['in'].source.value
            self._value = not in_
        return self._value

    def reset_value(self):
        self._value = None


class Constant(BasicElement):
    def __init__(self, constant_value: bool):
        super().__init__()
        self._constant_value = constant_value
        self._outs['out'] = []

    @property
    def value(self):
        return self._constant_value

    def reset_value(self):
        self._value = None


if __name__ == "__main__":
    constant = Constant(False)
    or_gate = OrGate(num_inputs=2)

    connection = Connection(constant, 'out', or_gate, 'in1')
    or_gate.set_input_connection('in1', connection)
    constant.set_output_connection('out', connection)

    print(or_gate.value)
