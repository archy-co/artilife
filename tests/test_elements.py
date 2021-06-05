import unittest
import sys

sys.path.append("..")     # to run tests from tests directory directly

from elements import Connection
from elements import Constant, Variable
from elements import BasicLogicGate
from elements import AndGate, OrGate, NotGate, XorGate, NandGate, NorGate
from elements import Multiplexer, Encoder, Decoder, FullAdder, AdderSubtractor, RightShifter
from elements import GatedSRFlipFlop as SRFlipFlop


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
        self.assertEqual(self.true_constant.calc_value()['out'], True)
        self.assertEqual(self.false_constant.calc_value()['out'], False)

        self.assertEqual(self.true_constant.element_type, 'CONSTANT')
        self.assertEqual(self.false_constant.element_type, 'CONSTANT')

    def test_variable(self):
        self.assertEqual(self.variable.calc_value(), {"out": False})
        self.variable.switch()
        self.assertEqual(self.variable.calc_value(), {"out": True})
        self.variable.switch()
        self.assertEqual(self.variable.calc_value(), {"out": False})

    def test_and(self):
        self.assertEqual(self.and_gate.calc_value()['out'], False)

        connection = Connection(self.true_constant, 'out', self.and_gate, 'in1')
        self.true_constant.set_output_connection(connection)
        self.and_gate.set_input_connection(connection)
        self.assertEqual(self.and_gate.calc_value()['out'], False)

        connection = Connection(self.false_constant, 'out', self.and_gate, 'in2')
        self.true_constant.set_output_connection(connection)
        self.and_gate.set_input_connection(connection)
        self.assertEqual(self.and_gate.calc_value()['out'], False)

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
        self.assertEqual(el.calc_value(), {'out': True})
        el = self._create_element_with_constants(OrGate, [False, False, False])
        self.assertEqual(el.calc_value(), {'out': False})

        constant = Constant("c0", constant_value=True)
        connection = Connection(constant, "out", self.or_gate, "in1")
        constant.set_output_connection(connection)
        self.or_gate.set_input_connection(connection)

        self.assertEqual(self.or_gate.calc_value(), {'out': True})

    def test_xor(self):
        el = self._create_element_with_constants(XorGate, [False, False, False])
        self.assertEqual(el.calc_value(), {'out': False})
        el = self._create_element_with_constants(XorGate, [True, False, False])
        self.assertEqual(el.calc_value(), {'out': True})
        el = self._create_element_with_constants(XorGate, [True, True, False])
        self.assertEqual(el.calc_value(), {'out': False})
        el = self._create_element_with_constants(XorGate, [True, True, False])
        self.assertEqual(el.calc_value(), {'out': False})

    def test_nand(self):
        el = self._create_element_with_constants(NandGate, [False, True])
        self.assertEqual(el.calc_value(), {'out': True})
        el = self._create_element_with_constants(NandGate, [False, False, False])
        self.assertEqual(el.calc_value(), {'out': True})
        el = self._create_element_with_constants(NandGate, [True, False, False])
        self.assertEqual(el.calc_value(), {'out': True})
        el = self._create_element_with_constants(NandGate, [True] * 1000)
        self.assertEqual(el.calc_value(), {'out': False})

    def test_nor(self):
        el = self._create_element_with_constants(NorGate, [False, True])
        self.assertEqual(el.calc_value(), {'out': False})
        el = self._create_element_with_constants(NorGate, [False, False, False])
        self.assertEqual(el.calc_value(), {'out': True})
        el = self._create_element_with_constants(NorGate, [True, False, False])
        self.assertEqual(el.calc_value(), {'out': False})
        el = self._create_element_with_constants(NorGate, [False] * 10)
        self.assertEqual(el.calc_value(), {'out': True})

        constant = Constant("c0", constant_value=True)
        connection = Connection(constant, "out", self.nor_gate, "in1")
        constant.set_output_connection(connection)
        self.nor_gate.set_input_connection(connection)

        self.assertEqual(self.nor_gate.calc_value(), {'out': False})

    def test_not(self):
        not_gate = NotGate("not_gate0")
        self.assertEqual(not_gate.calc_value(), {'out': None})

        constant = Constant("c0", constant_value=True)
        connection = Connection(constant, "out", not_gate, "in")
        constant.set_output_connection(connection)
        not_gate.set_input_connection(connection)


        self.assertEqual(not_gate.calc_value(), {'out': False})

    def test_multi_and(self):
        num_inputs = 1000
        multi_and = AndGate('and1', num_inputs=num_inputs)
        self.assertFalse(multi_and.calc_value()['out'])
        self.assertEqual(multi_and.element_type, "AND")
        for i in range(1, num_inputs+1):
            constant = Constant(f'const{i}', constant_value=True)
            connection = Connection(constant, 'out', multi_and, 'in' + str(i))
            constant.set_output_connection(connection)
            multi_and.set_input_connection(connection)

            if i == num_inputs:
                self.assertTrue(multi_and.calc_value()['out'])
            else:
                self.assertFalse(multi_and.calc_value()['out'])

    def test_multiplexer(self):
        multiplexer = Multiplexer('multiplexer1', num_select_lines=1)

        self.assertEqual(multiplexer.calc_value()['out'], None)

        constant = Constant('constant', constant_value=False)
        connection = Connection(constant, 'out', multiplexer, 'in1')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)


        self.assertEqual(multiplexer.calc_value()['out'], None)

        constant = Constant('constant', constant_value=False)
        connection = Connection(constant, 'out', multiplexer, 'in2')
        multiplexer.set_input_connection(connection)
        constant.set_output_connection(connection)


        self.assertEqual(multiplexer.calc_value()['out'], False)
        self.assertEqual(multiplexer.element_type, "MULTIPLEXER")

    def test_encoder(self):
        encoder = Encoder('encoder', num_output_lines=1)

        self.assertEqual(encoder.calc_value(), {'output line 1': None})

        constant = Constant('constant', constant_value=True)
        connection = Connection(constant, 'out', encoder, 'input line 1')
        encoder.set_input_connection(connection)
        constant.set_output_connection(connection)


        self.assertEqual(encoder.calc_value(), {'output line 1': None})

        constant = Constant('constant', constant_value=True)
        connection = Connection(constant, 'out', encoder, 'input line 2')
        encoder.set_input_connection(connection)
        constant.set_output_connection(connection)


        self.assertEqual(encoder.calc_value(), {'output line 1': True})

        self.assertEqual(encoder.element_type, "ENCODER")

    def test_decoder(self):
        decoder = Decoder('decoder', num_input_lines=1)

        self.assertEqual(decoder.calc_value(), {'output line 1': None, 'output line 2': None})

        constant = Constant('constant', constant_value=True)
        connection = Connection(constant, 'out', decoder, 'input line 1')
        decoder.set_input_connection(connection)
        constant.set_output_connection(connection)


        self.assertEqual(decoder.calc_value(), {'output line 1': False, 'output line 2': True})

        constant = Constant('constant', constant_value=False)
        connection = Connection(constant, 'out', decoder, 'input line 1')
        decoder.set_input_connection(connection)
        constant.set_output_connection(connection)


        self.assertEqual(decoder.calc_value(), {'output line 1': True, 'output line 2': False})

        self.assertEqual(decoder.element_type, "DECODER")

    def test_fulladder(self):
        fullAdder = FullAdder('full adder 1')

        self.assertEqual(fullAdder.calc_value(), {'Cout': None, 'S': None})

        constant = Constant("c1", constant_value=True)
        connection = Connection(constant, 'out', fullAdder, 'A')
        constant.set_output_connection(connection)
        fullAdder.set_input_connection(connection)


        self.assertEqual(fullAdder.calc_value(), {'Cout': None, 'S': None})

        constant = Constant("c2", constant_value=True)
        connection = Connection(constant, 'out', fullAdder, 'Cin')
        constant.set_output_connection(connection)
        fullAdder.set_input_connection(connection)


        self.assertEqual(fullAdder.calc_value(), {'Cout': None, 'S': None})

        constant = Constant("c3", constant_value=True)
        connection = Connection(constant, 'out', fullAdder, 'B')
        constant.set_output_connection(connection)
        fullAdder.set_input_connection(connection)


        self.assertEqual(fullAdder.calc_value(), {'Cout': True, 'S': True})

    def test_addersubtractor(self):
        addersubtractor = AdderSubtractor("Adder-subtractor1", num_bits=2)

        self.assertEqual(addersubtractor.calc_value(), {"S0": None, "S1": None, "Cout": None})

        constant = Constant('c1', constant_value=False)
        connection = Connection(constant, "out", addersubtractor, "A0")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)


        self.assertEqual(addersubtractor.calc_value(), {"S0": None, "S1": None, "Cout": None})

        constant = Constant('c1', constant_value=True)
        connection = Connection(constant, "out", addersubtractor, "B1")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)

        constant = Constant('c1', constant_value=False)
        connection = Connection(constant, "out", addersubtractor, "B0")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)

        constant = Constant('c1', constant_value=False)
        connection = Connection(constant, "out", addersubtractor, "A1")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)

        constant = Constant('c1', constant_value=False)
        connection = Connection(constant, "out", addersubtractor, "sub")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)


        self.assertEqual(addersubtractor.calc_value(), {"S0": False, "S1": True, "Cout": False})

        constant = Constant('c1', constant_value=True)
        connection = Connection(constant, "out", addersubtractor, "sub")
        constant.set_output_connection(connection)
        addersubtractor.set_input_connection(connection)


        self.assertEqual(addersubtractor.calc_value(), {"S0": False, "S1": True, "Cout": False})

    def test_right_shifter(self):
        right_shifter = RightShifter(id_="rightShifter1", num_bits=2)
        self.assertEqual(right_shifter.calc_value(), {'out0': None, 'out1': None})

        constant = Constant('c1', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': None, 'out1': None})

        constant = Constant('c1', constant_value=False)
        connection = Connection(constant, 'out', right_shifter, 'shift_line0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': None, 'out1': None})

        constant = Constant('c1', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line1')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': None, 'out1': None})

        constant = Constant('c2', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': False, 'out1': True})

        constant = Constant('c3', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': True, 'out1': True})

    def test_right_shifter4(self):
        right_shifter = RightShifter(id_="rightShifter1")
        self.assertEqual(right_shifter.calc_value(), {'out0': False, 'out1': False, 'out2': False, 'out3': False})

        constant = Constant('c1', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line1')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': False, 'out1': False, 'out2': False, 'out3': False})

        constant = Constant('c2', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in3')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': False, 'out1': False, 'out2': False, 'out3': False})

        constant = Constant('c3', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in2')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': False, 'out1': False, 'out2': False, 'out3': True})

        constant = Constant('c4', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in2')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': False, 'out1': False, 'out2': False, 'out3': True})

        constant = Constant('c5', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'in0')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': False, 'out1': True, 'out2': False, 'out3': True})

        constant = Constant('c6', constant_value=True)
        connection = Connection(constant, 'out', right_shifter, 'shift_line3')
        constant.set_output_connection(connection)
        right_shifter.set_input_connection(connection)


        self.assertEqual(right_shifter.calc_value(), {'out0': False, 'out1': True, 'out2': False, 'out3': True})

    @staticmethod
    def _connect_two_elements(element1, output, element2, input_):
        connection = Connection(element1, output, element2, input_)
        element1.set_output_connection(connection)
        element2.set_input_connection(connection)

    def test_sr_flipflop(self):
        flip_flop = SRFlipFlop("id0", enable_state=True)

        self.assertEqual(flip_flop.calc_value()['Q'], True)

        constant = Constant('c0', constant_value=True)
        self._connect_two_elements(constant, 'out', flip_flop, 'S')

        self.assertEqual(flip_flop.calc_value(), {'Q': True})

        constant = Constant('c1', constant_value=False)
        self._connect_two_elements(constant, 'out', flip_flop, 'S')

        self.assertEqual(flip_flop.calc_value(), {'Q': True})

        constant = Constant('c2', constant_value=True)
        self._connect_two_elements(constant, 'out', flip_flop, 'R')

        self.assertEqual(flip_flop.calc_value(), {'Q': False})

        constant = Constant('c3', constant_value=False)
        self._connect_two_elements(constant, 'out', flip_flop, 'R')

        self.assertEqual(flip_flop.calc_value(), {'Q': False})

        constant = Constant('c4', constant_value=True)
        self._connect_two_elements(constant, 'out', flip_flop, 'S')
        constant = Constant('c5', constant_value=True)
        self._connect_two_elements(constant, 'out', flip_flop, 'R')
        self.assertEqual(flip_flop.calc_value(), {'Q': False})


        constant = Constant('c4', constant_value=False)
        self._connect_two_elements(constant, 'out', flip_flop, 'S')
        constant = Constant('c5', constant_value=False)
        self._connect_two_elements(constant, 'out', flip_flop, 'R')

        self.assertTrue(flip_flop.calc_value()['Q'] in [True, False])

        flip_flop1 = SRFlipFlop("id1")
        self.assertTrue(flip_flop1.calc_value()['Q'] in [True, False])

    def test_sequential(self):
        nor1 = NorGate("nor1")
        nor2 = NorGate("nor1")
        v1 = Variable('v1')
        v2 = Variable('v2')


        print(nor1._truth_table)

        connection = Connection(v1, 'out', nor1, 'in1')
        v1.set_output_connection(connection)
        nor1.set_input_connection(connection)

        connection = Connection(v2, 'out', nor2, 'in2')
        v2.set_output_connection(connection)
        nor2.set_input_connection(connection)

        connection = Connection(nor1, 'out', nor2, 'in1')
        nor1.set_output_connection(connection)
        nor2.set_input_connection(connection)

        connection = Connection(nor2, 'out', nor1, 'in2')
        nor2.set_output_connection(connection)
        nor1.set_input_connection(connection)
        self.assertEqual(nor1.calc_value(), {'out': False})
        self.assertEqual(nor2.calc_value(), {'out': False})

        v1.switch()
        v1.calc_value()
        self.assertEqual(nor1.calc_value(), {'out': True})
        self.assertEqual(nor2.calc_value(), {'out': False})


if __name__ == "__main__":
    unittest.main()
