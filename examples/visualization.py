from schemdraw import logic
import schemdraw

d = schemdraw.Drawing()

and_start = logic.And(inputs=3, label='START')
and_final = logic.And(inputs=2, label='END')

print(and_final.__dict__)

# and_start.anchor('out').at(and_final.anchors['in1'])

and_final.anchor('out').at(and_start.anchors['in1'])
# and_final.anchor('in1').at(and_start.anchors['in2'])
# and_final.anchor('in2').at(and_start.anchors['in3'])

# and_start.at(and_final.anchors['in1'])

d += and_final
d += and_start # .anchor('in1')


# d.draw(backend='matplotlib')

# while True:
#     inps = int(input("Enter num of inps: "))
#     d += logic.And(inputs=inps)
#     d.draw(backend='matplotlib')

d.save('schematic.svg')