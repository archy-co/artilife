from schemdraw import logic
import schemdraw

d = schemdraw.Drawing()
and1 = logic.And(inputs=3)

print(and1.__dict__)

and2 = logic.And(inputs=2)
and2.at(and1.anchors['in1'])

d += and1
d += and2 # .anchor('in1')


d.draw(backend='matplotlib')

# while True:
#     inps = int(input("Enter num of inps: "))
#     d += logic.And(inputs=inps)
#     d.draw(backend='matplotlib')

# d.save('schematic.svg')