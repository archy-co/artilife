from schemdraw import logic
from schemdraw import elements as sd_elem
import schemdraw
import elements
from scheme import Scheme
from custom_elements import Constant

cell_width = 1.5
cell_length = 1.5


def visualize(scheme):
    elems = {}
    elems_match = {'AND': logic.And,
                   'OR': logic.Or,
                   'XOR': logic.Xor,
                   'NAND': logic.Nand,
                   'NOR': logic.Nor,
                   'NOT': logic.Not,
                   'CONSTANT': Constant,
                   'MULTIPLEXER': sd_elem.Multiplexer,
                   'ENCODER': None,
                   'DECODER': None,
                   'FULLADDER': None,
                   'ADDERSUBTRACTOR': None}

    # create and add to visual all elements
    d = schemdraw.Drawing()
    for scheme_element in scheme:
        start_coordinates = ((scheme_element.position[0] - 1) * cell_length,
                             (scheme_element.position[1] - 0.5) * cell_width)
        visual_element = elems_match[scheme_element.element_type]() \
            .label(str(scheme_element.id)).at(start_coordinates)
        elems[scheme_element.id] = d.add(visual_element)

    # add input connections for all elements
    for element in scheme:
        for in_label, in_connection in element.ins.items():
            source = elems[in_connection.source.id]
            destination = elems[in_connection.destination.id]

            # TODO: create {scheme_label: sd_label} or change labels
            #  names in sd elements
            line = sd_elem.Line().endpoints(
                source.absanchors[in_connection.output_label],
                destination.absanchors[in_connection.input_label])
            d.add(line)

    # add output values for terminal elements
    for element_id, free_outs in scheme.run().items():
        for label, value in free_outs.items():
            print(elems[element_id].__dict__)
            elems[element_id].label(label='0', loc='right')
            # elems[element_id].label(label=str(value), loc=label)

    # draw scheme
    d.draw(backend='matplotlib')


if __name__ == "__main__":
    s = Scheme()

    s.add_element('constant', 0, (1, 1),
                  constant_value=1)
    s.add_element('constant', 1, (1, 3), constant_value=1)
    s.add_element('and', 2, (3, 2))

    s.add_connection(0, 'out', 2, 'in2')
    s.add_connection(1, 'out', 2, 'in1')

    # print(s.run())
    visualize(s)
