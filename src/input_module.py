"""input module"""
from src.scheme import Scheme


class InputParser:
    def __init__(self, scheme: Scheme):
        self._scheme = scheme
        self._match_kwargs = {'v': 'constant_value',
                              's': 'num_select_lines',
                              'o': 'num_output_lines',
                              'i': 'num_input_lines',
                              'b': 'num_bits'}
        self._match_scheme_commands = {'add': self._scheme.add_element,
                                       'del': self._scheme.delete_element,
                                       'switch': None,
                                       '>': self._scheme.add_connection,
                                       '!>': self._scheme.delete_connection}
        self._match_num_main_params = {'add': 5,
                                       'del': 2,
                                       'switch': 2,
                                       '>': 5,
                                       '!>': 5}

    def parse_raw_input(self, input_str):
        """
        The user have to use specific set of commands to be able
        to interact with program.
        These commands includes: 'add', 'del', 'switch' for elements
        and '>', '!>' for connections.

        For adding a new element user should use command as follows:
            add *element_type* *id(name)* *cor1* *cor2* -*option_parameter* *value*
            , where 'cor1' and 'cor2' are x and y coordinates accordingly.
        Examples:
            add and 0 20 20
            add or 1 3 4
            add constant const_1 -10 15 -v 0
            add addersubtractor addsub_down 5 7 -b 2
        Next elements have optional parameters:
            constant
            -v: its value (0 or 1)
            multiplexer
            -s: number of lines to select
            encoder
            -o: number of output lines
            decoder
            -i: number of input lines
            addersubtractor
            -b: number of bits
            shifter
            -b: number of bits
        For deleting existing element user should use command as follows:
            del *id(name)*
        Examples:
            del 0
            del 1
        For adding new connection between elements user should use next command:
            *id1(name)* *output_label1* > *id2(name)* *input_label1*
        Example:
            0 out > 1 in1
        For deleting existing connection between elements user should use next command:
            *id1(name)* *output_label1* !> *id2(name)* *input_label1*
        Example:
            0 out !> 1 in1
        For switching the value of the variable source of signal:
            switch *id_of_variable_element*
        """

        parts = input_str.strip().split()

        if parts[0] in self._match_scheme_commands:
            command = parts[0]
        elif parts[2] in self._match_scheme_commands:
            command = parts[2]
        else:
            raise Exception('This command doesn\'t exist')

        num_main_params = self._match_num_main_params[command]
        kwargs = {}
        if len(parts) > num_main_params:
            args_values = parts[num_main_params:]
            for i in range(int(len(args_values) / 2)):
                arg = args_values[2 * i].strip('-')
                value = args_values[2 * i + 1]
                kwargs[self._match_kwargs[arg]] = int(value)

        if command == 'add':
            self._scheme.add_element(parts[1], parts[2],
                                     (int(parts[3]), int(parts[4])), **kwargs)
        elif command == 'del':
            self._scheme.delete_element(parts[1])
        elif command == 'switch':
            self._scheme[parts[1]].switch()
        elif command == '>':
            self._scheme.add_connection(parts[0], parts[1], parts[3], parts[4])
        elif command == '!>':
            self._scheme.delete_connection(parts[0], parts[1], parts[3], parts[4])
