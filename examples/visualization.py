from schemdraw import logic
import schemdraw


d = schemdraw.Drawing()
d.push()
d += logic.And()
d.pop()
d += logic.Or()
d.draw()

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

# d = schemdraw.Drawing()
#
# and_start = logic.And(inputs=3, label='START')
# and_final = logic.And(inputs=2, label='END').label(label='label', loc='bottom')
#
# print(and_final.__dict__)
#
# # and_start.anchor('out').at(and_final.anchors['in1'])
#
# and_final.anchor('out').at(and_start.anchors['in1'])
# # and_final.anchor('in1').at(and_start.anchors['in2'])
# # and_final.anchor('in2').at(and_start.anchors['in3'])
#
# # and_start.at(and_final.anchors['in1'])
#
# and_start.label(label='0', loc='out')
#
# d += and_final
# d += and_start # .anchor('in1')



# d.draw(backend='matplotlib')

# while True:
#     inps = int(input("Enter num of inps: "))
#     d += logic.And(inputs=inps)
#     d.draw(backend='matplotlib')

# d.save('schematic.svg')