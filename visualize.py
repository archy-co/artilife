from schemdraw import logic
from schemdraw import elements as sd_elem
import schemdraw
from custom_elements import Constant
from scheme import Scheme


class Visualizer:
    cell_width = 1.5
    cell_length = 1.5
    elements_match = {'AND': logic.And,
                      'OR': logic.Or,
                      'XOR': logic.Xor,
                      'NAND': logic.Nand,
                      'NOR': logic.Nor,
                      'NOT': logic.Not,
                      'CONSTANT': Constant,
                      'MULTIPLEXER': sd_elem.Multiplexer,
                      'ENCODER': sd_elem.Ic,
                      'DECODER': sd_elem.Ic,
                      'FULLADDER': sd_elem.Ic,
                      'ADDERSUBTRACTOR': sd_elem.Ic,
                      'SHIFTER': sd_elem.Ic}

    @staticmethod
    def _add_visual_elements(scheme, drawing):
        visual_elements = {}

        scheme_elements_outs = scheme.run()

        for scheme_element in scheme:
            # create element
            start_coordinates = (
                (scheme_element.position[0] - 1) * Visualizer.cell_length,
                (scheme_element.position[1] - 0.5) * Visualizer.cell_width)
            # get kwargs
            kwargs = Visualizer.get_elements_kwargs(scheme_element)
            visual_element = Visualizer.elements_match[
                scheme_element.element_type](**kwargs).label(str(scheme_element.id)).at(
                start_coordinates)

            # configure element
            if scheme_element.id in scheme_elements_outs:
                for label, value in scheme_elements_outs[scheme_element.id].items():
                    visual_element.label(label=str(int(value)), loc=label)

            # add element to visualization
            visual_elements[scheme_element.id] = drawing.add(visual_element)

        return visual_elements

    @staticmethod
    def get_elements_kwargs(scheme_element):
        kwargs = {}

        if scheme_element.element_type == "CONSTANT":
            kwargs['constant_value'] = scheme_element.value['out']

        if scheme_element.element_type == "MULTIPLEXER":
            kwargs['pins'] = []
            num_select_lines = scheme_element.number_select_lines
            for i in range(1, num_select_lines + 1):
                kwargs['pins'].append(sd_elem.IcPin(name=f'sel{i}', anchorname=f'select line {i}', side='B'))
            for i in range(1, 2 ** num_select_lines + 1):
                kwargs['pins'].append(sd_elem.IcPin(name=f'in{i}', anchorname=f'input line {i}', side='L'))
            kwargs['pins'].append(sd_elem.IcPin(name='out', side='R'))

        elif scheme_element.element_type == "ENCODER":
            kwargs['pins'] = []
            num_output_lines = scheme_element.number_output_lines
            for i in range(1, num_output_lines + 1):
                kwargs['pins'].append(sd_elem.IcPin(name=f'out{i}', anchorname=f'output line {i}', side='right'))
            for i in range(1, 2 ** num_output_lines + 1):
                kwargs['pins'].append(sd_elem.IcPin(name=f'in{i}', anchorname=f'input line {i}', side='left'))

        elif scheme_element.element_type == "DECODER":
            kwargs['pins'] = []
            num_input_lines = scheme_element.number_input_lines
            for i in range(1, num_input_lines + 1):
                kwargs['pins'].append(sd_elem.IcPin(name=f'in{i}', anchorname=f'input line {i}', side='left'))
            for i in range(1, 2 ** num_input_lines + 1):
                kwargs['pins'].append(sd_elem.IcPin(name=f'out{i}', anchorname=f'output line {i}', side='right'))

        elif scheme_element.element_type == "FULLADDER":
            kwargs['pins'] = [sd_elem.IcPin(name='A', side='left'),
                              sd_elem.IcPin(name='B', side='left'),
                              sd_elem.IcPin(name='Cin', side='left'),
                              sd_elem.IcPin(name='S', side='right'),
                              sd_elem.IcPin(name='Cout', side='right')]

        elif scheme_element.element_type == "ADDERSUBTRACTOR":
            kwargs['pins'] = []
            num_bits = scheme_element.number_bits
            for i in range(num_bits):
                kwargs['pins'].append(sd_elem.IcPin(name=f'A{i}', side='left'))
            for i in range(num_bits):
                kwargs['pins'].append(sd_elem.IcPin(name=f'B{i}', side='left'))
            kwargs['pins'].append(sd_elem.IcPin(name=f'sub', side='left'))
            for i in range(num_bits):
                kwargs['pins'].append(sd_elem.IcPin(name=f'S{i}', side='right'))
            kwargs['pins'].append(sd_elem.IcPin(name=f'Cout', side='right'))

        elif scheme_element.element_type == "SHIFTER":
            kwargs['pins'] = []
            num_bits = scheme_element.number_bits
            for i in range(num_bits):
                kwargs['pins'].append(sd_elem.IcPin(name=f'in{i}', side='left'))
            for i in range(num_bits):
                kwargs['pins'].append(sd_elem.IcPin(name=f'sh{i}', anchorname=f'shift_line{i}', side='left'))
            for i in range(num_bits):
                kwargs['pins'].append(sd_elem.IcPin(name=f'out{i}', side='right'))

        return kwargs

    @staticmethod
    def _add_input_connections(scheme, visual_elements, drawing):
        for element in scheme:
            for in_label, in_connection in filter(lambda x: x[1] is not None, element.ins.items()):
                source = visual_elements[in_connection.source.id]
                destination = visual_elements[in_connection.destination.id]

                # TODO: match sd and elements labels: {scheme_label: sd_label}
                #  or change labels names in default sd elements
                #  ! or create custom elements with the same names of anchors
                line = sd_elem.Line().endpoints(
                    source.absanchors[in_connection.output_label],
                    destination.absanchors[in_connection.input_label])
                drawing.add(line)

    @staticmethod
    def visualize(scheme):
        drawing = schemdraw.Drawing()

        # configure and add visual elements
        visual_elements = Visualizer._add_visual_elements(scheme, drawing)

        Visualizer._add_input_connections(scheme, visual_elements, drawing)

        drawing.draw(backend='matplotlib')


if __name__ == "__main__":
    s = Scheme()

    # simple scheme

    # s.add_element('constant', 0, (1, 2),
    #               constant_value=1)
    # s.add_element('constant', 1, (1, 4), constant_value=1)
    # s.add_element('xor', 2, (3, 4))
    # s.add_element('and', 3, (3, 2))
    #
    # s.add_connection(0, 'out', 2, 'in2')
    # s.add_connection(0, 'out', 3, 'in2')
    # s.add_connection(1, 'out', 2, 'in1')
    # s.add_connection(1, 'out', 3, 'in1')

    # test multiplexer, encoder

    # s.add_element('constant', 0, (1, 1),
    #               constant_value=1)
    # # s.add_element('multiplexer', 1, (3, 1), num_select_lines=4)
    # # s.add_element('encoder', 1, (3, 1), num_output_lines=4)
    # s.add_element('decoder', 1, (3, 1), num_input_lines=4)
    #
    # s.add_connection(0, 'out', 1, 'input line 4')

    # test fulladder, addersub

    # s.add_element('constant', 0, (1, 1),
    #               constant_value=1)
    # s.add_element('constant', 1, (1, 2),
    #               constant_value=1)
    # s.add_element('constant', 2, (1, 3),
    #               constant_value=0)
    # # s.add_element('fulladder', 3, (3, 1))
    # s.add_element('addersubtractor', 3, (3, 1), num_bits=1)
    #
    # s.add_connection(0, 'out', 3, 'A0')
    # s.add_connection(1, 'out', 3, 'B0')
    # s.add_connection(2, 'out', 3, 'sub')

    # test shifter

    s.add_element('constant', 0, (1, 1),
                  constant_value=1)
    s.add_element('constant', 1, (1, 2),
                  constant_value=1)
    s.add_element('constant', 2, (1, 3),
                  constant_value=1)
    s.add_element('shifter', 3, (3, 1), num_bits=4)

    s.add_connection(0, 'out', 3, 'in2')
    s.add_connection(1, 'out', 3, 'in3')
    s.add_connection(2, 'out', 3, 'shift_line1')

    # print(s.run())
    Visualizer.visualize(s)
