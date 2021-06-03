"""input module"""


def raw_input(scheme, command):
    """
    The user have to use specific set of commands to be able
    to interact with program.
    These commands includes 'add', 'del' for elements and '>', '!>' for connection.

    For adding a new element user should use command as follows:
        add *element_type* *id(name)* *cor1* *cor2*, where 'cor1' and 'cor2'
        are x and y coordinates accordingly.
    Examples:
        add and 0 20 20
        add or 1 3 4
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
    """

    line = command.strip().split()
    if line[0] == 'add':
        scheme.add_element(line[1], line[2], (int(line[3]), int(line[4])))
    elif line[0] == 'del':
        scheme.delete_element(line[1])
    elif '>' in line:
        scheme.add_connection(line[0], line[1], line[3], line[4])
    elif '!>' in line:
        scheme.delete_connection(line[0], line[1], line[3], line[4])
