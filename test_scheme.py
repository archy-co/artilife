from scheme import Scheme
from scheme import IdIsAlreadyTakenError
from scheme import NoSuchOutputLabelError
from scheme import NoSuchInputLabelError
from scheme import NoSuchIdError
import unittest


class TestScheme(unittest.TestCase):
    def setUp(self):
        self.scheme = Scheme()

    def test_general(self):
        self.assertTrue(len(self.scheme._elements) == 0)
        self.scheme.add_element('and', 1)
        self.scheme.add_element('or', 2)
        self.assertTrue(len(self.scheme._elements) == 2)
        self.scheme.delete_element(1)
        self.assertRaises(NoSuchIdError, self.scheme.delete_element, 1)
        self.assertTrue(len(self.scheme._elements) == 1)
        self.scheme.add_element('constant', 1)

        self.scheme.add_element('xor', 3, 4)
        elem3 = self.scheme._elements[3]
        self.assertTrue(len(elem3.ins) == 4)

        self.scheme.add_element('constant', 4, False)
        elem4 = self.scheme._elements[4]
        self.assertFalse(elem3.value['out'])

    def test_connections(self):
        self.scheme.add_element('constant', 1)
        self.scheme.add_element('or', 2)
        elem1 = self.scheme._elements[1]
        elem2 = self.scheme._elements[2]

        self.assertEqual(elem1.outs[list(elem1.outs.keys())[0]], [])
        self.assertIsNone(elem2.ins['in1'])

        self.scheme.add_connection(1, 'out', 2, 'in1')

        self.assertNotEqual(elem1.outs[list(elem1.outs.keys())[0]], [])
        self.assertIsNotNone(elem2.ins['in1'])
        self.assertTrue(elem2.ins['in1'] in elem1.outs[list(elem1.outs.keys())[0]])

        self.scheme.delete_connection(elem1, 'out', elem2, 'in1')

        self.assertEqual(elem1.outs[list(elem1.outs.keys())[0]], [])
        self.assertIsNone(elem2.ins['in1'])

        self.scheme.add_element('and', 3)
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

    def test_run(self):
        self.scheme.add_element('constant', 1, 1)
        self.scheme.add_element('constant', 2, 0)
        self.scheme.add_element('or', 3, 2)
        self.scheme.add_element('and', 4, 2)
        self.scheme.add_connection(1, 'out', 3, 'in1')
        self.scheme.add_connection(2, 'out', 3, 'in2')
        self.scheme.add_connection(1, 'out', 4, 'in1')
        self.scheme.add_connection(2, 'out', 4, 'in2')
        self.assertEqual(list(list(self.scheme.run().values())[0][0].values())[0], 1)
        self.assertEqual(list(list(self.scheme.run().values())[1][0].values())[0], 0)



if __name__ == "__main__":
    unittest.main()
