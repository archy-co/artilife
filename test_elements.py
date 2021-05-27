import unittest

from elements import Connection
from elements import Constant
from elements import AndGate, OrGate, NotGate, XorGate, NandGate, NorGate


class TestElements(unittest.TestCase):
    def setUp(self):
        self.true_constant = Constant(True)
        self.false_constant = Constant(False)
        self.and_gate = AndGate(2)
        self.or_gate = OrGate(2)
        self.not_gate = NotGate()
        self.xor_gate = XorGate(2)
        self.nand_gate = NandGate(2)
        self.nor_gate = NorGate(2)

    def test_constant(self):
        self.assertEquals(self.true_constant.value['out'], True)
        self.assertEquals(self.false_constant.value['out'], False)

    def test_and(self):
        self.assertEquals(self.and_gate.value['out'], False)

        connection = Connection(self.true_constant, 'out', self.and_gate, 'in1')
        self.true_constant.set_output_connection('out', connection)
        self.and_gate.set_input_connection('in1', connection)
        self.assertEquals(self.and_gate.value['out'], False)

        connection = Connection(self.false_constant, 'out', self.and_gate, 'in2')
        self.true_constant.set_output_connection('out', connection)
        self.and_gate.set_input_connection('in2', connection)
        self.assertEquals(self.and_gate.value['out'], False)

    def test_multi_and(self):
        num_inputs = 1000
        multi_and = AndGate(num_inputs=num_inputs)
        self.assertFalse(multi_and.value['out'])
        for i in range(1, num_inputs+1):
            constant = Constant(True)
            input_label = 'in' + str(i)
            connection = Connection(constant, 'out', multi_and, input_label)
            constant.set_output_connection('out', connection)
            multi_and.set_input_connection(input_label, connection)
            multi_and.reset_value()
            if i == num_inputs:
                self.assertTrue(multi_and.value['out'])
            else:
                self.assertFalse(multi_and.value['out'])



if __name__ == "__main__":
    unittest.main()
