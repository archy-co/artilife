'''
Experimentation module

Represents scheme from #1 (https://github.com/archy-co/l4logic/issues/1)
'''
import sys
from scheme import Scheme
sys.setrecursionlimit(10)

scheme1 = Scheme()
scheme1.add_element('Constant', 1, (1, 1))
scheme1.add_element('Constant', 2, (1, 2), constant_value=False)

scheme1.add_element('NOR', 3, (2, 1))
scheme1.add_element('NOR', 4, (2, 2))

scheme1.add_element('NOT', 5, (3, 1))
scheme1.add_element('NOT', 6, (3, 2))
scheme1.add_element('NOT', 7, (3, 3))

const1 = scheme1[1]
const0 = scheme1[2]
xor1 = scheme1[3]
xor2 = scheme1[4]
not1 = scheme1[5]
not2 = scheme1[6]

scheme1.add_connection(1, 'out', 3, 'in1')
scheme1.add_connection(2, 'out', 4, 'in1')
scheme1.add_connection(3, 'out', 4, 'in2')
scheme1.add_connection(4, 'out', 3, 'in2')
scheme1.add_connection(3, 'out', 5, 'in')
scheme1.add_connection(4, 'out', 6, 'in')
scheme1.add_connection(1, 'out', 7, 'in')

print(scheme1.run())
