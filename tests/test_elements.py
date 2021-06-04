import unittest
import sys

sys.path.append("..")     # to run tests from tests directory directly

from src.elements import Connection
from src.elements import Constant, Variable
from src.elements import BasicLogicGate
from src.elements import AndGate, OrGate, NotGate, XorGate, NandGate, NorGate
from src.elements import Multiplexer, Encoder, Decoder, FullAdder, AdderSubtractor, RightShifter
from src.elements import GatedSRFlipFlop as SRFlipFlop


class TestElements(unittest.TestCase):
    def setUp(self):
        self.true_constant = Constant("true constant", constant_value=True)
        self.false_constant = Constant("false constant", constant_value=False)
        self.variable = Variable("variable", init_value=False)
        self.and_gate = AndGate("and gate", num_inputs=2)
        self.or_gate = OrGate('or gate', num_inputs=2)
        self.not_gate = NotGate('not gate')
        self.xor_gate = XorGate('xor gate', num_inputs=2)
        self.nand_gate = NandGate('nand gate', num_inputs=2)
        self.nor_gate = NorGate('nor gate', num_inputs=2)

    def test_constant(self):
        self.assertEqual(self.true_constant.value['out'], True)
        self.assertEqual(self.false_constant.value['out'], False)

        self.assertEqual(self.true_constant.element_type, 'CONSTANT')
        self.assertEqual(self.false_constant.element_type, 'CONSTANT')

    def test_variable(self):
        self.assertEqual(self.variable.value, {"out": False})
        self.variable.switch()
        self.assertEqual(self.variable.value, {"out": True})
        self.variable.switch()
        self.assertEqual(self.variable.value, {"out": False})

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

        self.assertEqual(self.and_gate.element_type, "AND")

    @staticmethod
    def _create_element_with_constants(type_, constants):
        """Helper method
        type_ must be a class which inherits from BasicLogicGate.
        constants must be a list of boolean values.
        """
        element = type_(id_="1", num_inputs=len(constants))
        for idx, val in enumerate(constants):
            constant = Constant("c"+str(idx), constant_value=val)
            conn = Connection(constant, 'out', element, 'in' + str(idx+1))
            constant.set_output_connection(conn)
            element.set_input_connection(conn)
        return element

    def test_or(self):
        el = self._create_element_with_constants(OrGate, [True, False, True, True, False, False])
        self.assertEqual(el.value, {'out': True})
        el = self._create_element_with_constants(OrGate, [False, False, False])
        self.assertEqual(el.value, {'out': False})

    def test_xor(self):
        el = self._create_element_with_constants(XorGate, [False, False, False])
        self.assertEqual(el.value, {'out': False})
        el = self._create_element_with_constants(XorGate, [True, False, False])
        self.assertEqual(el.value, {'out': True})
        el = self._create_element_with_constants(XorGate, [True, True, False])
        self.assertEqual(el.value, {'out': False})
        el = self._create_element_with_constants(XorGate, [True, True, False])
        self.assertEqual(el.value, {'out': False})

    def test_nand(self):
        el = self._create_element_with_constants(NandGate, [False, True])
        self.assertEqual(el.value, {'out': True})
        el = self._create_element_with_constants(NandGate, [False, False, False])
        self.assertEqual(el.value, {'out': True})
        el = self._create_element_with_constants(NandGate, [True, False, False])
        self.assertEqual(el.value, {'out': True})
        el = self._create_element_with_constants(NandGate, [True] * 1000)
        self.assertEqual(el.value, {'out': False})

    def test_nor(self):
        el = self._create_element_with_constants(NorGate, [False, True])
        self.assertEqual(el.value, {'out': False})
        el = self._create_element_with_constants(NorGate, [False, False, False])
        self.assertEqual(el.value, {'out': True})
        el = self._create_element_with_constants(NorGate, [True, False, False])
        self.assertEqual(el.value, {'out': False})
        el = self._create_element_with_constants(NorGate, [False] * 1000)
        self.assertEqual(el.value, {'out': True})

    def test_not(self):
        not_gate = NotGate("not_gate0")
        self.assertEqual(not_gate.value, {'out': True})

        constant = Constant("c0", constant_value=True)
        connection = Connection(constant, "out", not_gate, "in")
        constant.set_output_connection(connection)
        not_gate.set_input_connection(connection)

        not_gate.reset_value()
        self.assertEqual(not_gate.value, {'out': False})

    def test_multi_and(self):
        num_inputs = 1000
        multi_and = AndGate('and1', num_inputs=num_inputs)
        self.assertFalse(multi_and.value['out'])
        self.assertEqual(multi_and.element_type, "AND")
        for i in range(1, num_inputs+1):
            constant = Constant(f'const{i}', constant_value=True)
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

        constant = Constant('constant', constant_value=True)
        connection = Connection(constant, 'out', multiplexer, 'in1')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)

        multiplexer.reset_value()
        self.assertEqual(multiplexer.value['out'], True)

        constant = Constant('constant', constant_value=False)
        connection = Connection(constant, 'out', multiplexer, 'in2')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)

        multiplexer.reset_value()
        self.assertEqual(multiplexer.value['out'], True)

        constant = Constant('constant', constant_value=True)
        connection = Connection(constant, 'out', multiplexer, 'sel1')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)

        multiplexer.reset_value()
        self.assertEqual(multiplexer.value['out'], False)

        constant = Constant('constant', constant_value=False)
        connection = Connection(constant, 'out', multiplexer, 'sel1')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)

        multiplexer.reset_value()
        self.assertEqual(multiplexer.value['out'], True)
        self.assertEqual(multiplexer.element_type, "MULTIPLEXER")

    def test_encoder(self):
        encoder = Encoder('encoder', num_output_lines=1)

        self.assertEqual(encoder.value, {'output line 1': False})

        constant = Constant('constant', constant_value=True)
        connection = Connection(constant, 'out', encoder, 'input line 1')
        encoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        encoder.reset_value()
        self.assertEqual(encoder.value, {'output line 1': False})

        constant = Constant('constant', constant_value=False)
        connection = Connection(constant, 'out', encoder, 'input line 1')
        encoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        encoder.reset_value()
        self.assertEqual(encoder.value, {'output line 1': False})

        constant = Constant('constant', constant_value=True)
        connection = Connection(constant, 'out', encoder, 'input line 2')
        encoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        encoder.reset_value()
        self.assertEqual(encoder.value, {'output line 1': True})

        self.assertEqual(encoder.element_type, "ENCODER")

    def test_decoder(self):
        decoder = Decoder('decoder', num_input_lines=1)

        self.assertEqual(decoder.value, {'output line 1': True, 'output line 2': False})

        constant = Constant('constant', constant_value=True)
        connection = Connection(constant, 'out', decoder, 'input line 1')
        decoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        decoder.reset_value()
        self.assertEqual(decoder.value, {'output line 1': False, 'output line 2': True})

        constant = Constant('constant', constant_value=False)
        connection = Connection(constant, 'out', decoder, 'input line 1')
        decoder.set_input_connection(connection)
        constant.set_output_connection(connection)

        decoder.reset_value()
        self.assertEqual(decoder.value, {'output line 1': True, 'output line 2': False})

        self.assertEqual(decoder.element_type, "DECODER")

    def test_fulladder(self):
        fullAdder = FullAdder('full adder 1')

        self.assertEqual(fullAdder.value, {'Cout': False, 'S': False})

        constant = Constant("c1", constant_value=True)
        connection = Connection(constant, 'out', fullAdder, 'A')
        constant.set_output_connection(connection)
        fullAdder.set_input_connection(connection)

        fullAdder.reset_value()
        self.assertEqual(fullAdder.value, {'Cout': False, 'S': True})

        constant = Constant("c2", constant_value=True)
        connection = Connection(constant, 'out', fullAdder, 'Cin')
        constant.set_output_connection(connection)
        fullAdder.set_input_connection(connection)

        fullAdder.reset_value()
        self.assertEqual(fullAdder.value, {'Cout': True, 'S': False})

        constant = Constant("c3", constant_value=True)
        connection = Connection(constant, 'out', fullAdder, 'B')
        constant.set_output_connection(connection)
        fullAdder.set_input_connection(connection)

        fullAdder.reset_value()
        self.assertEqual(fullAdder.value, {'Cout': True, 'S': True})

    def test_addersubtractor(self):
        addersubtractor = AdderSubtractor("Adder-subtractor1", num_bits=2)

        self.assertEqual(addersubtractor.value, {"S0": False, "S1": False, "Cout": False})

        constant = Constant('c1', constant_value=False)
        connection = Connection(constant, "out", addersubtractor, "A0")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)

        addersubtractor.reset_value()
        self.assertEqual(addersubtractor.value, {"S0": False, "S1": False, "Cout": False})

        constant = Constant('c1', constant_value=True)
        connection = Connection(constant, "out", addersubtractor, "B1")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)

        self.assertEqual(addersubtractor.value, {"S0": False, "S1": False, "Cout": False})
        addersubtractor.reset_value()
        self.assertEqual(addersubtractor.value, {"S0": False, "S1": True, "Cout": False})

        constant = Constant('c1', constant_value=True)
        connection = Connection(constant, "out", addersubtractor, "sub")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)

        addersubtractor.reset_value()
        self.assertEqual(addersubtractor.value, {"S0": False, "S1": True, "Cout": False})

    def test_right_shifter(self):
        right_shifter = RightShifter(id_="rightShifter1", num_bits=2)
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': False})

        constant = Constant('c1', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': False})

        constant = Constant('c2', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': True, 'out1': False})

        constant = Constant('c3', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line1')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': True, 'out1': True})

        constant.delete_output_connection('out')
        right_shifter.delete_input_connection('shift_line0')

        constant = Constant('c4', constant_value=False)
        connection = Connection(constant, 'out', right_shifter, 'shift_line0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': True})

    def test_right_shifter4(self):
        right_shifter = RightShifter(id_="rightShifter1")
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': False, 'out2': False, 'out3': False})

        constant = Constant('c1', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line1')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': False, 'out2': False, 'out3': False})

        constant = Constant('c2', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in3')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': False, 'out2': False, 'out3': False})

        constant = Constant('c3', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in2')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': False, 'out2': False, 'out3': True})

        constant = Constant('c4', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in2')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': False, 'out2': False, 'out3': True})

        constant = Constant('c5', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': True, 'out2': False, 'out3': True})

        constant = Constant('c6', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line3')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)

        right_shifter.reset_value()
        self.assertEqual(right_shifter.value, {'out0': False, 'out1': True, 'out2': False, 'out3': True})

    @staticmethod
    def _connect_two_elements(element1, output, element2, input_):
        connection = Connection(element1, output, element2, input_)
        element1.set_output_connection(connection)
        element2.set_input_connection(connection)

    def test_sr_flipflop(self):
        flip_flop = SRFlipFlop("id0", enable_state=True)

        self.assertEqual(flip_flop.value['Q'], True)

        constant = Constant('c0', constant_value=True)
        self._connect_two_elements(constant, 'out', flip_flop, 'S')
        flip_flop.reset_value()
        self.assertEqual(flip_flop.value, {'Q': True})

        constant = Constant('c1', constant_value=False)
        self._connect_two_elements(constant, 'out', flip_flop, 'S')
        flip_flop.reset_value()
        self.assertEqual(flip_flop.value, {'Q': True})

        constant = Constant('c2', constant_value=True)
        self._connect_two_elements(constant, 'out', flip_flop, 'R')
        flip_flop.reset_value()
        self.assertEqual(flip_flop.value, {'Q': False})

        constant = Constant('c3', constant_value=False)
        self._connect_two_elements(constant, 'out', flip_flop, 'R')
        flip_flop.reset_value()
        self.assertEqual(flip_flop.value, {'Q': False})

        constant = Constant('c4', constant_value=True)
        self._connect_two_elements(constant, 'out', flip_flop, 'S')
        constant = Constant('c5', constant_value=True)
        self._connect_two_elements(constant, 'out', flip_flop, 'R')
        self.assertEqual(flip_flop.value, {'Q': False})
        flip_flop.reset_value()

        constant = Constant('c4', constant_value=False)
        self._connect_two_elements(constant, 'out', flip_flop, 'S')
        constant = Constant('c5', constant_value=False)
        self._connect_two_elements(constant, 'out', flip_flop, 'R')
        flip_flop.reset_value()
        self.assertTrue(flip_flop.value['Q'] in [True, False])

        flip_flop1 = SRFlipFlop("id1")
        self.assertTrue(flip_flop1.value['Q'] in [True, False])


if __name__ == "__main__":
    unittest.main()
