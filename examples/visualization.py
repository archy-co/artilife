from schemdraw import logic
import schemdraw
from schemdraw import elements as sd_elem

table_unit = 3

# d = schemdraw.Drawing()
# # d.push()
# # cell_coordinates = (table_unit * 1, table_unit * 0.5)
# # d += logic.And().at(cell_coordinates)
# # d.pop()
# # cell_coordinates = (table_unit * 0, table_unit * 0.5)
# # # at() sets element beginning position
# # d += logic.Or().at(cell_coordinates)
# elems = {}
# for i in range(10):
#     cell_coordinates = (table_unit * i, table_unit * 0.5)
#     elems[i] = d.add(logic.And().at(cell_coordinates))
# 
# elems[0].color('red')
# elems[1].color('blue')
# print(elems[0].__dict__, elems[1].__dict__, sep="\n")
# line = sd_elem.Line().endpoints(elems[0].absanchors['out'],
#                                 elems[1].absanchors['in1'])
# line = d.add(line)
# line.color('green')
# 
# d.pop()
# 
# d.add(sd_elem.CPE())
# 
# d.draw()

# ------------------------------

# d = schemdraw.Drawing()
# d += logic.Line().length(d.unit/4).label('R', 'left')
# d += (G1 := logic.Nor().anchor('in1'))
# d += logic.Line().length(d.unit/4)
# d += (Q := logic.Dot())
# d += logic.Line().length(d.unit/4).label('Q', 'right')
#
# # removed at() -> horrible
# d += (G2 := logic.Nor().at((G1.in1[0],G1.in1[1]-2.5)).anchor('in1'))
# d += logic.Line().length(d.unit/4)
# d += (Qb := logic.Dot())
# d += logic.Line().length(d.unit/4).label('$\overline{Q}$', 'right')
# d += (S1 := logic.Line().up().at(G2.in1).length(d.unit/6))
# d += logic.Line().down().at(Q.start).length(d.unit/6)
# d += logic.Line().to(S1.end)
# d += (R1 := logic.Line().down().at(G1.in2).length(d.unit/6))
# d += logic.Line().up().at(Qb.start).length(d.unit/6)
# d += logic.Line().to(R1.end)
# d += logic.Line().left().at(G2.in2).length(d.unit/4).label('S', 'left')
#
# d.save('schematic.svg')
#
# d.draw()


# first try

d = schemdraw.Drawing()

and_start = logic.And(inputs=3, label='START')
and_final = logic.And(inputs=2, label='END').label(label='label', loc='bottom')

print(and_final.__dict__)

and_final.anchor('out').at(and_start.anchors['in1'])



d += and_final
and_start = d.add(and_start)

# don't work because can't change labels after set to drawing
and_start.label(label='0', loc='out')
and_start.color('red')

d.draw(backend='matplotlib')
