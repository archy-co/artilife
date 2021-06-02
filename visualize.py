from pprint import pprint

from schemdraw import logic
from schemdraw import elements as sd_elem
import schemdraw
from custom_elements import Constant
from scheme import Scheme
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from typing import Dict, Union, List
import elements


class Visualizer:
    """Visualize scheme elements with schemdraw library"""

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
    default_label_size = 8

    @staticmethod
    def _add_visual_elements(scheme: Scheme, drawing: schemdraw.Drawing,
                             iterate_circuit: bool = False) -> Dict[
        str, sd_elem.Element]:
        """Add visual elements to drawing and return dictionary
        with added elements

        Arguments
        ----------
            iterate_circuit: specifies if to calculate output for image
            and iterate circuit
        """
        visual_elements = {}

        if iterate_circuit:
            scheme_elements_outs = scheme.run()

        for scheme_element in scheme:
            # create visual element
            start_coordinates = (
                scheme_element.position[0],
                scheme_element.position[1])
            # create integrated circuit visual element custom attributes
            # depending on element type
            kwargs = Visualizer._create_elements_kwargs(scheme_element)
            visual_element = Visualizer.elements_match[
                scheme_element.element_type](**kwargs)
            if 'center' not in visual_element.anchors:
                visual_element.anchors['center'] = (0, 0)
            visual_element = visual_element.label(
                str(scheme_element.id), color='blue', loc='center').anchor(
                'center').at(start_coordinates)

            # configure element outputs
            # set labels now because after element is added to drawing
            # you can't change their labels
            if iterate_circuit:
                if scheme_element.id in scheme_elements_outs:
                    for label, value in scheme_elements_outs[
                        scheme_element.id].items():
                        visual_element.label(label=str(int(value)), loc=label,
                                             color='green')

            # add element to drawing
            visual_elements[scheme_element.id] = drawing.add(visual_element)

        return visual_elements

    @staticmethod
    def _create_elements_kwargs(scheme_element: elements.BasicElement) -> Dict[
        str, Union[bool, List[sd_elem.IcPin]]]:
        """Create custom attributes for integrated
        circuits elements"""

        kwargs = {}

        if Visualizer.elements_match[scheme_element.element_type] == sd_elem.Ic:
            kwargs['plblsize'] = Visualizer.default_label_size

        if scheme_element.element_type == "CONSTANT":
            kwargs['constant_value'] = scheme_element.value['out']
            kwargs['lbl_size'] = Visualizer.default_label_size

        if scheme_element.element_type == "MULTIPLEXER":
            kwargs['pins'] = []
            num_select_lines = scheme_element.number_select_lines
            for i in range(1, num_select_lines + 1):
                kwargs['pins'].append(
                    sd_elem.IcPin(name=f'sel{i}', anchorname=f'select line {i}',
                                  side='B'))
            for i in range(1, 2 ** num_select_lines + 1):
                kwargs['pins'].append(
                    sd_elem.IcPin(name=f'in{i}', anchorname=f'input line {i}',
                                  side='L'))
            kwargs['pins'].append(sd_elem.IcPin(name='out', side='R'))

        elif scheme_element.element_type == "ENCODER":
            kwargs['pins'] = []
            num_output_lines = scheme_element.number_output_lines
            for i in range(1, num_output_lines + 1):
                kwargs['pins'].append(
                    sd_elem.IcPin(name=f'out{i}', anchorname=f'output line {i}',
                                  side='right'))
            for i in range(1, 2 ** num_output_lines + 1):
                kwargs['pins'].append(
                    sd_elem.IcPin(name=f'in{i}', anchorname=f'input line {i}',
                                  side='left'))

        elif scheme_element.element_type == "DECODER":
            kwargs['pins'] = []
            num_input_lines = scheme_element.number_input_lines
            for i in range(1, num_input_lines + 1):
                kwargs['pins'].append(
                    sd_elem.IcPin(name=f'in{i}', anchorname=f'input line {i}',
                                  side='left'))
            for i in range(1, 2 ** num_input_lines + 1):
                kwargs['pins'].append(
                    sd_elem.IcPin(name=f'out{i}', anchorname=f'output line {i}',
                                  side='right'))

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
                kwargs['pins'].append(
                    sd_elem.IcPin(name=f'sh{i}', anchorname=f'shift_line{i}',
                                  side='left'))
            for i in range(num_bits):
                kwargs['pins'].append(sd_elem.IcPin(name=f'out{i}', side='right'))

        return kwargs

    @staticmethod
    def _add_input_connections(scheme: Scheme,
                               visual_elements: Dict[str, sd_elem.Element],
                               drawing: schemdraw.Drawing):
        """Create visual input connections for elements"""
        for element in scheme:
            for in_label, in_connection in filter(lambda x: x[1] is not None,
                                                  element.ins.items()):
                source = visual_elements[in_connection.source.id]
                destination = visual_elements[in_connection.destination.id]

                line = sd_elem.Line().endpoints(
                    source.absanchors[in_connection.output_label],
                    destination.absanchors[in_connection.input_label])
                drawing.add(line)

    @staticmethod
    def get_tkinter_image(scheme: Scheme, max_width: int,
                          max_height: int,
                          iterate_circuit: bool = False) -> ImageTk.PhotoImage:
        """Return tkinter image for current scheme state

        Arguments
        ----------
            iterate_circuit: specifies if to calculate output for image
            and iterate circuit
        """
        drawing = schemdraw.Drawing(lw=1, fontsize=Visualizer.default_label_size)

        # configure and add visual elements
        visual_elements = Visualizer._add_visual_elements(scheme, drawing,
                                                          iterate_circuit)

        Visualizer._add_input_connections(scheme, visual_elements, drawing)

        # create custom axis
        fig, ax = plt.subplots()
        # ax.set_xlim(0, 25)
        # ax.set_ylim(0, 25)
        pixels_inch = 96
        axis_multiplier = 1.15
        inch_width, inch_height = int(max_width / pixels_inch * axis_multiplier), \
                                  int(max_height / pixels_inch * axis_multiplier)
        fig.set_size_inches((inch_width, inch_height))
        plt.grid()

        # to create fig object inside drawing
        # with custom axis and frame
        drawing.draw(showframe=True, show=False, ax=ax)

        image_bytes = drawing.get_imagedata('png')

        # test drawing
        # plt.show()

        # fix bug that schemdraw doesn't close matplotlib figures
        plt.close('all')

        image = Image.open(io.BytesIO(image_bytes))
        image = Visualizer._resize_img(image, max_width, max_height)
        image = ImageTk.PhotoImage(image)

        return image

    @staticmethod
    def _resize_img(image: Image, max_width: int, max_height: int) -> Image:
        """Resize image so that it fits in (max_width x max_height)"""
        if image.height <= max_height and image.width <= max_width:
            return image

        width_ratio = image.size[0] / max_width
        height_ratio = image.size[1] / max_height

        if width_ratio > height_ratio:
            fit_width = max_width
            fit_height = round(image.size[1] / width_ratio)
        else:
            fit_height = max_height
            fit_width = round(image.size[0] / height_ratio)

        fit_image = image.resize((fit_width, fit_height), Image.NEAREST)

        return fit_image


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

    # s.add_element('constant', 0, (1, 1),
    #               constant_value=1)
    # s.add_element('constant', 1, (1, 2),
    #               constant_value=1)
    s.add_element('constant', 2, (1, 3),
                  constant_value=1)
    s.add_element('shifter', 3, (3, 1), num_bits=4)
    # s.add_element('and', 4, (3, 3))

    # s.add_connection(0, 'out', 3, 'in2')
    # s.add_connection(1, 'out', 3, 'in3')
    # s.add_connection(2, 'out', 3, 'shift_line1')

    Visualizer.get_tkinter_image(s, 800, 800)
