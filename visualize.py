from schemdraw import logic
import schemdraw
import elements
from scheme import Scheme

def visualize(scheme):
    elems = {}
    elems_match = {'AndGate': logic.And,
                   'OrGate': logic.Or}
    # create all elements
    for element in scheme:
        elems[element.id] = elems_match[element.__class__.__name__](inputs=2,
                                                                    label=str(element.id))

    # add in connections for all elements
    for element in scheme:
        for in_label, in_connection in element._ins.items():
            source = elems[in_connection.source.id]
            destination = elems[in_connection.destination.id]

            source.anchor(in_connection.output_label).\
                at(destination.anchors[in_connection.input_label])

    # draw sceheme
    d = schemdraw.Drawing()
    for elem in elems.items():
        d += elem
    d.draw(backend='matplotlib')

if __name__ == "__main__":
    s = Scheme()

    s.add_element('Constant', element_id=0, constant_value=1)
    s.add_element('Constant', element_id=1, constant_value=1)
    s.add_element('AndGate', 2)

    s.add_connection(0, 'out', 2, 'in1')
    s.add_connection(1, 'out', 2, 'in2')

    visualize(s)