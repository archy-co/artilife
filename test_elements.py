import unittest

from elements import Connection
from elements import Constant
from elements import AndGate, OrGate, NotGate, XorGate, NandGate, NorGate
from elements import Multiplexer, Encoder, Decoder, FullAdder, AdderSubtractor, RightShifter


class TestElements(unittest.TestCase):
    def setUp(self):
        self.true_constant = Constant("true constant", True)
        self.false_constant = Constant("false constant", False)
        self.and_gate = AndGate("and gate", 2)
        self.or_gate = OrGate('or gate', 2)
        self.not_gate = NotGate('not gate')
        self.xor_gate = XorGate('xor gate', 2)
        self.nand_gate = NandGate('nand gate', 2)
        self.nor_gate = NorGate('nor gate', 2)

    def test_constant(self):
        self.assertEqual(self.true_constant.value['out'], True)
        self.assertEqual(self.false_constant.value['out'], False)

        self.assertEqual(self.true_constant.element_type, 'CONSTANT')
        self.assertEqual(self.false_constant.element_type, 'CONSTANT')

    def test_and(self):
        self.assertEqual(self.and_gate.value['out'], False)

        connection = Connection(self.true_constant, 'out', self.and_gate, 'in1')
        self.true_constant.set_output_connection(connection)
        self.and_gate.set_input_connection(connection)
        self.assertEqual(self.and_gate.value['out'], False)

        connection = Connection(self.false_constant, 'out', self.and_gate, 'in2')
        self.true_constant.set_output_connection(connection)
        self.and_gate.set_input_connection(connection)
        self.assertEqual(self.and_gate.value['out'], False)

        self.assertEqual(self.and_gate.element_type, "AND 2")

    def test_multi_and(self):
        num_inputs = 1000
        multi_and = AndGate('and1', num_inputs=num_inputs)
        self.assertFalse(multi_and.value['out'])
        self.assertEqual(multi_and.element_type, "AND 1000")
        for i in range(1, num_inputs+1):
            constant = Constant(f'const{i}', True)
            connection = Connection(constant, 'out', multi_and, 'in' + str(i))
            constant.set_output_connection(connection)
            multi_and.set_input_connection(connection)
            multi_and.reset_value()
            if i == num_inputs:
                self.assertTrue(multi_and.value['out'])
            else:
                self.assertFalse(multi_and.value['out'])

    def test_multiplexer(self):
        multiplexer = Multiplexer('multiplexer1', num_select_lines=1)

        self.assertEqual(multiplexer.value['out'], False)

        constant = Constant('constant', True)
        connection = Connection(constant, 'out', multiplexer, 'input line 1')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)

        multiplexer.reset_value()
        self.assertEqual(multiplexer.value['out'], True)

        constant = Constant('constant', False)
        connection = Connection(constant, 'out', multiplexer, 'input line 2')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)

        multiplexer.reset_value()
        self.assertEqual(multiplexer.value['out'], True)

        constant = Constant('constant', True)
        connection = Connection(constant, 'out', multiplexer, 'select line 1')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)

        multiplexer.reset_value()
        self.assertEqual(multiplexer.value['out'], False)

        constant = Constant('constant', False)
        connection = Connection(constant, 'out', multiplexer, 'select line 1')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)

        multiplexer.reset_value()
        self.assertEqual(multiplexer.value['out'], True)
        self.assertEqual(multiplexer.element_type, "MULTIPLEXER 1")

    def test_encoder(self):
        encoder = Encoder('encoder', num_output_lines=1)

        self.assertEqual(encoder.value, {'output line 1': False})

        constant = Constant('constant', True)
        connection = Connection(constant, 'out', encoder, 'input line 1')
        encoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        encoder.reset_value()
        self.assertEqual(encoder.value, {'output line 1': False})

        constant = Constant('constant', False)
        connection = Connection(constant, 'out', encoder, 'input line 1')
        encoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        encoder.reset_value()
        self.assertEqual(encoder.value, {'output line 1': False})

        constant = Constant('constant', True)
        connection = Connection(constant, 'out', encoder, 'input line 2')
        encoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        encoder.reset_value()
        self.assertEqual(encoder.value, {'output line 1': True})

        self.assertEqual(encoder.element_type, "ENCODER 1")

    def test_decoder(self):
        decoder = Decoder('decoder', num_input_lines=1)

        self.assertEqual(decoder.value, {'output line 1': True, 'output line 2': False})

        constant = Constant('constant', True)
        connection = Connection(constant, 'out', decoder, 'input line 1')
        decoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        decoder.reset_value()
        self.assertEqual(decoder.value, {'output line 1': False, 'output line 2': True})

        constant = Constant('constant', False)
        connection = Connection(constant, 'out', decoder, 'input line 1')
        decoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        decoder.reset_value()
        self.assertEqual(decoder.value, {'output line 1': True, 'output line 2': False})

        self.assertEqual(decoder.element_type, "DECODER 1")

    def test_fulladder(self):
        fullAdder = FullAdder('full adder 1')

        self.assertEqual(fullAdder.value, {'Cout': False, 'S': False})

        constant = Constant("c1", True)
        connection = Connection(constant, 'out', fullAdder, 'A')
        constant.set_output_connection(connection)
        fullAdder.set_input_connection(connection)

        fullAdder.reset_value()
        self.assertEqual(fullAdder.value, {'Cout': False, 'S': True})

        constant = Constant("c2", True)
        connection = Connection(constant, 'out', fullAdder, 'Cin')
        constant.set_output_connection(connection)
        fullAdder.set_input_connection(connection)

        fullAdder.reset_value()
        self.assertEqual(fullAdder.value, {'Cout': True, 'S': False})

        constant = Constant("c3", True)
        connection = Connection(constant, 'out', fullAdder, 'B')
        constant.set_output_connection(connection)
        fullAdder.set_input_connection(connection)

        fullAdder.reset_value()
        self.assertEqual(fullAdder.value, {'Cout': True, 'S': True})

    def test_addersubtractor(self):
        addersubtractor = AdderSubtractor("Adder-subtractor1", 2)

        self.assertEqual(addersubtractor.value, {"S0": False, "S1": False, "Cout": False})

        constant = Constant('c1', False)
        connection = Connection(constant, "out", addersubtractor, "A0")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)

        addersubtractor.reset_value()
        self.assertEqual(addersubtractor.value, {"S0": False, "S1": False, "Cout": False})

        constant = Constant('c1', True)
        connection = Connection(constant, "out", addersubtractor, "B1")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)

        self.assertEqual(addersubtractor.value, {"S0": False, "S1": False, "Cout": False})
        addersubtractor.reset_value()
        self.assertEqual(addersubtractor.value, {"S0": False, "S1": True, "Cout": False})

        constant = Constant('c1', True)
        connection = Connection(constant, "out", addersubtractor, "sub")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)

        addersubtractor.reset_value()
        self.assertEqual(addersubtractor.value, {"S0": False, "S1": True, "Cout": False})

    def test_right_shifter(self):
        right_shifter = RightShifter(id_="rightShifter1", num_bits=2)
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': False})

        constant = Constant('c1', True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': False})

        constant = Constant('c2', True)
        connection = Connection(constant, 'out', right_shifter, 'in0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': True, 'out1': False})

        constant = Constant('c3', True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line1')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': True, 'out1': True})

        constant.delete_output_connection('out')
        right_shifter.delete_input_connection('shift_line0')

        constant = Constant('c4', False)
        connection = Connection(constant, 'out', right_shifter, 'shift_line0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': True})


if __name__ == "__main__":
    unittest.main()
