import elements

class IdIsAlreadyTakenError(Exception):
    def __init__(self, id):
        self.message = f'ID <{id}> is already taken'
        super().__init__(self.message)

class NoSuchIdError(Exception):
    def __init__(self, id):
        self.message = f'There\'s no element with ID <{id}>'
        super().__init__(self.message)

class NoSuchOutputLabelError(Exception):
    def __init__(self, output_label):
        self.message = f'There\'s no <{output_label}> output label'
        super().__init__(self.message)

class NoSuchInputLabelError(Exception):
    def __init__(self, input_label):
        self.message = f'There\'s no <{input_label}> input label'
        super().__init__(self.message)


class Scheme:
    '''
    ADT Scheme that contains elements
    '''
    def __init__(self):
        self._elements = []

    def add_element(self, element_type, element_id):
        element_type_to_class_dct = {
            'multiplexer': elements.Multiplexer,
            'and': elements.AndGate,
            'or': elements.OrGate,
            'not': elements.NotGate,
            'nor': elements.NorGate,
            'xor': elements.XorGate,
            'nand': elements.NandGate,
            'constant': elements.Constant,
            'decoder': elements.Decoder,
            'encoder': elements.Encoder,
        }
        if not self._validate_id(element_id):
            raise IdIsAlreadyTakenError(element_id)
        new_element = element_type_to_class_dct[element_type](element_id, 2)

        new_element.id = element_id
        self._elements.append(new_element)

    def _validate_id(self, id: str) -> bool:
        '''
        Checks if the <id> is already assigned to an element in <self._elements>
        Return:  True if id is available
                 False if id is already taken
        '''
        for element in self._elements:
            if element.id == id:
                return False
        return True

    def add_connection(self, source_id, output_label, destination_id, input_label):
        '''
        Add connection from *output_label* output of element with id *source_id*
        to *input_label* input of element with id *destination_id* if validation
        is successful

        If there is no such output label / input label, corresponding Exception
        will be raised
        '''
        source = self._get_by_id(source_id)
        destination = self._get_by_id(destination_id)

        connection = elements.Connection(source, output_label, destination, input_label)
        # self._validate_connection(connection)

        try:
            source.set_output_connection(connection)
        except KeyError:
            raise NoSuchOutputLabelError(output_label)

        try:
            destination.set_input_connection(connection)
        except KeyError:
            raise NoSuchInputLabelError(input_label)


    def _get_by_id(self, element_id: str) -> elements.BasicElement:
        for element in self._elements:
            if element.id == element_id:
                return element

    def delete_element(self, element_id: str):
        '''
        Deletes element from scheme with all conections. Corresponding connections
        of connected elements are set to None
        '''
        element = self._get_by_id(element_id)
        if element is None:
            raise NoSuchIdError(element_id)
        for _out in element.outs:
            for out_connection in element.outs[_out]:
                out_connection.source.delete_output_connection(out_connection.output_label)
                out_connection.destination.delete_input_connection(out_connection.input_label)

        for _in in element.ins:
            in_connection = element.ins[_in]
            if in_connection is None:
                break
            in_connection.source.delete_output_connection(in_connection.output_label)
            in_connection.destination.delete_input_connection(in_connection.input_label)

        self._elements.remove(element)

    def delete_connection(self, source: elements.BasicElement, output_label,
                           destination: elements.BasicElement, input_label):
        '''
        Deletes connection between elements by deliting source output and destination input
        '''
        source.delete_output_connection(output_label)
        destination.delete_input_connection(input_label)

    def _validate_connection(self):
        raise NotImplementedError

    def run(self):
        self._reset()


    def __iter__(self):
        return iter(self._elements)

    def _reset(self):
        for element in self._elements:
            if isinstance(element, BasicLogicGate):
                element.reset_value()

    def __str__(self):
        return str(self._elements)

