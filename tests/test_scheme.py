'''
Test module for Scheme
'''
import unittest
import sys

sys.path.append("..")     # to run tests from tests directory directly

from scheme import Scheme
from scheme import IdIsAlreadyTakenError
from scheme import NoSuchOutputLabelError
from scheme import NoSuchInputLabelError
from scheme import NoSuchIdError


class TestScheme(unittest.TestCase):
    def setUp(self):
        self.scheme = Scheme()

    def test_general(self):
        self.assertTrue(len(self.scheme._elements) == 0)
        self.scheme.add_element('and', 1, (2, 1))
        self.scheme.add_element('or', 2, (2, 3))
        self.assertTrue(len(self.scheme._elements) == 2)
        self.scheme.delete_element(1)
        self.assertRaises(NoSuchIdError, self.scheme.delete_element, 1)

        self.assertRaises(IdIsAlreadyTakenError, self.scheme.add_element, 'and', 2, (4, 1))
        self.assertTrue(len(self.scheme._elements) == 1)
        self.scheme.add_element('constant', 1, position=(1, 2))

        self.scheme.add_element('xor', 3, num_inputs=4, position=(1, 5))
        elem3 = self.scheme._elements[3]
        self.assertTrue(len(elem3.ins) == 4)

        self.scheme.add_element('constant', 4, False)
        elem4 = self.scheme._elements[4]
        self.assertFalse(elem3.value['out'])
        self.assertEqual(len(list(self.scheme.__iter__())), 4)

    def test_connections(self):
        self.scheme.add_element('constant', 1, position=(1, 1))
        self.scheme.add_element('or', 2, position=(1, 2))
        elem1 = self.scheme._elements[1]
        elem2 = self.scheme._elements[2]

        self.assertEqual(elem1.outs[list(elem1.outs.keys())[0]], [])
        self.assertIsNone(elem2.ins['in1'])

        self.assertRaises(NoSuchOutputLabelError, self.scheme.add_connection, 1, 'out1', 2, 'in2')
        self.assertRaises(NoSuchInputLabelError, self.scheme.add_connection, 1, 'out', 2, 'in5')
        self.scheme.add_connection(1, 'out', 2, 'in1')

        self.assertNotEqual(elem1.outs[list(elem1.outs.keys())[0]], [])
        self.assertIsNotNone(elem2.ins['in1'])
        self.assertTrue(elem2.ins['in1'] in elem1.outs[list(elem1.outs.keys())[0]])

        self.scheme.delete_connection(1, 'out', 2, 'in1')

        self.assertEqual(elem1.outs[list(elem1.outs.keys())[0]], [])
        self.assertIsNone(elem2.ins['in1'])

        self.scheme.add_element('and', 3, position=(1, 4))
        elem3 = self.scheme._elements[3]

        self.scheme.add_connection(1, 'out', 3, 'in1')
        self.assertTrue(elem3.ins['in1'] in elem1.outs[list(elem1.outs.keys())[0]])
        self.assertNotEqual(elem1.outs[list(elem1.outs.keys())[0]], [])
        self.scheme.delete_element(3)

        self.assertFalse(3 in self.scheme._elements)
        self.assertEqual(elem1.outs[list(elem1.outs.keys())[0]], [])

        self.scheme.add_connection(1, 'out', 2, 'in1')
        self.assertTrue(elem2.ins['in1'] in elem1.outs[list(elem1.outs.keys())[0]])
        self.scheme.clear()
        self.assertEqual(elem1.outs[list(elem1.outs.keys())[0]], [])
        self.assertIsNone(elem2.ins['in1'])
        self.assertTrue(len(self.scheme._elements) == 0)

        # delete unexisting connection
        self.scheme.add_element('constant', 1, position=(4, 2))
        self.scheme.add_element('xor', 2, position=(5, 2))
        t_elem1 = self.scheme._elements[1]
        t_elem2 = self.scheme._elements[2]

        self.assertEqual(t_elem1.outs['out'], [])
        self.scheme.delete_connection(1, 'out', 2, 'in1')
        self.assertEqual(t_elem1.outs['out'], [])


    def test_run(self):
        self.scheme.add_element('constant', 1, constant_value=True, position=(1, 1))
        self.scheme.add_element('constant', 2, constant_value=False, position=(1, 2))
        self.scheme.add_element('or', 3, position=(1, 3))
        self.scheme.add_element('and', 4, position=(1, 4))
        self.scheme.add_connection(1, 'out', 3, 'in1')
        self.scheme.add_connection(2, 'out', 3, 'in2')
        self.scheme.add_connection(1, 'out', 4, 'in1')
        self.scheme.add_connection(2, 'out', 4, 'in2')
        self.assertTrue(self.scheme.run()[3]['out'])
        self.assertFalse(self.scheme.run()[4]['out'])

    def test_move(self):
        self.scheme.add_element('constant', 1, position=(1, 1))
        self.scheme.add_element('not', 2, position=(1, 2))

        self.scheme.move(1, (2, 2))

        self.assertEqual(self.scheme._elements[1].position, (2, 2))


if __name__ == "__main__":
    unittest.main()
