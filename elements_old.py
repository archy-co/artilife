class ElementConnection:
    def __init__(self, destination):
        self.source = None
        self.destination = destination


class BasicElement:
    def __init__(self):
        self.connections = {'out': []}

    def set_out_connection(self, other, input_number):
        other.connections[input_number].source = self

    def calculate_output(self):
        pass


class Constant(BasicElement):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def calculate_output(self):
        return self.value


class ToggleSwitch(BasicElement):
    def __init__(self):
        super().__init__()
        self.value = 0

    def calculate_output(self):
        return self.value

    def flip_switch(self):
        self.value = (self.value + 1) % 2


class AndGate(BasicElement):
    def __init__(self):
        super().__init__()
        self.connections['in1'] = ElementConnection(destination=self)
        self.connections['in2'] = ElementConnection(destination=self)

    def calculate_output(self):
        return self.connections['in1'].source.calculate_output() \
               and self.connections['in2'].source.calculate_output()


if __name__ == "__main__":
    el_const0 = Constant(0)
    el_const1 = Constant(1)
    el_switch = ToggleSwitch()
    el_and = AndGate()
    el_switch.set_out_connection(el_and, 'in1')
    el_switch.set_out_connection(el_and, 'in2')
    print(el_and.calculate_output())
    el_switch.flip_switch()
    print(el_and.calculate_output())
