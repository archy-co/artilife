"""
truth_table.py

A module containing the implemetation of truth table and truth tables of the logic elements.
"""

import ctypes
from typing import Dict, Callable


class TruthTable:
    """A class for the truth table of logical function.
    Methods
    -------
    get_value(vars)
        Given a list of boolean values, return the value that was calculated by the logical function.
    predict_value(vars)
        Given a dictionary that maps some names of the variables to their values,
        return the value of the function if possible.
    """
    def __init__(self, var_names: list, function: Callable):
        """Initialize a truth table with the names of variables and the logical function.
        """
        self._num_vars = len(var_names)
        self._data = (ctypes.py_object * 2**self._num_vars)() # stores data
        self._names_to_nums = {name: num for num, name in enumerate(reversed(var_names))} # map from names of variables to some numbers
        self._nums_to_names = {num: name for name, num in self._names_to_nums.items()} # reverse map

        for i in range(2**self._num_vars):
            self._data[i] = function(self._int_to_binary(i, self._num_vars))

    @staticmethod
    def _int_to_binary(integer, num_bits):
        binary_repr = []
        while integer != 0:
            integer, remainder = divmod(integer, 2)
            binary_repr.append(bool(remainder))

        while len(binary_repr) != num_bits:
            binary_repr.append(False)

        binary_repr.reverse()

        return binary_repr

    def get_value(self, vars):
        idx = sum(vars[i] * 2**(self._num_vars-i-1) for i in range(self._num_vars))
        return self._data[idx]

    def predict_value(self, incomplete_vars: Dict[str, bool]):
        """Given a dictionary that maps names of some of the variables to their values, return:
        1. True or False if all unspecified variables are nonessential.
        2. None if some of missed values of variables are essential.
        """
        incomplete_vars = {key: val for key, val in incomplete_vars.items() if val is not None}
        first_index = sum(incomplete_vars[i] * 2**self._names_to_nums[i] for i in incomplete_vars)

        num_missed_vars = self._num_vars - len(incomplete_vars)
        missed = []
        for name in self._names_to_nums:
            if name not in incomplete_vars:
                missed.append(2**self._names_to_nums[name])

        value = None
        for i in range(2**num_missed_vars):
            is_included = self._int_to_binary(i, num_missed_vars)
            cur_index = first_index + sum(missed[j] for j in range(num_missed_vars) if is_included[j])
            cur_value = self._data[cur_index]
            if value == None:
                value = cur_value
            elif value != cur_value:
                return
        return value

    def __str__(self):
        str_repr = ""
        for i in range(2**self._num_vars):
            vars_values = self._int_to_binary(i, self._num_vars)
            cur_row = f"{i:0{self._num_vars}b} "
            cur_row += str(self.get_value(vars_values))
            str_repr += cur_row + "\n"
        return str_repr

    @classmethod
    def get_multiplexer_truth_table(cls, num_select_lines):
        def mux_func(lst_args):
            idx = 0
            for i in range(num_select_lines):
                idx += 2**i * lst_args[i]
            return bool(lst_args[num_select_lines+idx])
        var_names = [f"sel{i+1}" for i in range(num_select_lines)] + [f"in{i+1}" for i in range(2**num_select_lines)]
        return cls(var_names, mux_func)

    @classmethod
    def get_encoder_truth_table(cls, num_output_lines):
        def encoder_func(lst_args):
            out = [False] * num_output_lines
            for input_line in range(2**num_output_lines):
                if lst_args[input_line] == True:
                    binary = cls._int_to_binary(input_line, num_output_lines)
                    for idx, val in enumerate(binary[::-1]):
                        out[idx] = out[idx] or val
            return dict(zip([f"output line {i+1}" for i in range(num_output_lines)], out))
        var_names = [f"input line {i+1}" for i in range(2**num_output_lines)]
        return cls(var_names, encoder_func)

    @classmethod
    def get_decoder_truth_table(cls, num_input_lines):
        def decoder_func(lst_args):
            decoded = 0
            for input_line in range(num_input_lines):
                decoded += lst_args[input_line] * 2**input_line
            out = {f"output line {i+1}": False for i in range(2**num_input_lines)}
            out[f"output line {decoded+1}"] = True
            return out
        var_names = [f"input line {i+1}" for i in range(num_input_lines)]
        return cls(var_names, decoder_func)

    @classmethod
    def get_fulladder_truth_table(cls):
        def fulladder_func(lst_args):
            bitA = lst_args[0]
            bitB = lst_args[1]
            carry_in = lst_args[2]
            return {'S': (bitA != bitB) != carry_in,
                    'Cout': (bitA and bitB) or (bitA and carry_in) or (bitB and carry_in)}

        return cls(['A', 'B', 'Cin'], fulladder_func)

    @classmethod
    def get_addersubtractor_truth_table(cls, num_bits):
        def addersubtractor_func(lst_args):
            sub = lst_args[-1]
            number_A = lst_args[:num_bits]
            number_B = lst_args[num_bits: 2*num_bits]

            if sub:
                for idx, val in enumerate(number_B):
                    number_B[idx] = not number_B[idx]

            out = {}
            carry = sub
            for i in range(num_bits):
                out["S" + str(i)] = (number_A[i] != number_B[i]) != carry
                carry = (number_A[i] and number_B[i]) or (number_A[i] and carry) or (number_B[i] and carry)
            out['Cout'] = carry
            return out

        var_names = [f'A{i}' for i in range(num_bits)]
        var_names.extend([f'B{i}' for i in range(num_bits)])
        var_names.append('sub')

        return cls(var_names, addersubtractor_func)

    @classmethod
    def get_rightshifter_truth_table(cls, num_bits):
        def rightshifter_func(lst_args):
            out = {}
            to_shift = lst_args[:num_bits]
            shift_by = lst_args[num_bits:]
            for i in range(num_bits):
                out[f"out{i}"] = False
                for j in range(i + 1):
                    out[f"out{i}"] = out[f"out{i}"] or (to_shift[i - j] and shift_by[j])
            return out
        var_names = [f'in{i}' for i in range(num_bits)]
        var_names.extend([f'shift_line{i}' for i in range(num_bits)])

        return cls(var_names, rightshifter_func)


if __name__ == "__main__":
    print(TruthTable.get_rightshifter_truth_table(2))
    # print(TruthTable.get_rightshifter_truth_table(2).predict_value({}))
