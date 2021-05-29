from schemdraw import logic
import schemdraw
from schemdraw import elements as elm

# d = schemdraw.Drawing()
#
# and_start = logic.And(inputs=3, label='START')
# and_final = logic.And(inputs=2, label='END')
#
# # print(and_final.__dict__)
#
# and_start.anchor('out').at(and_final.anchors['in1'])
# and_start.anchor('out').at(and_final.anchors['in2'])
#
# and_final.label(label='0', loc='out')
#
# d += and_final
# d += and_start

# d.draw(backend='matplotlib')

d1 = schemdraw.Drawing()
d1 += elm.Resistor()
d1.push()
d1 += elm.Capacitor().down()
d1 += elm.Line().left()
d1.pop()

d2 = schemdraw.Drawing()   # Add a second drawing
for i in range(3):
    d2 += elm.ElementDrawing(d1)   # Add the first drawing to it 3 times
d2.draw(backend='matplotlib')

