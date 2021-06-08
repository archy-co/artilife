"""
truth_table.py

A module containing the implemetation of truth table and truth tables of the logic elements.
"""

from typing import List, Dict, Callable
import itertools

import pandas as pd
import numpy as np


class TruthTable:
    """A class for the truth table of logical function.
    Methods
    -------
    get_value(vars)
        Given a list of boolean values, return the value that was calculated by the logical function.
    predict_value(args)
        Given a dictionary that maps some names of the arguments to their values,
        return the value of the function if possible.
    """
    def __init__(self, arg_names: list, out_names: list, function: Callable[[List[bool]], List[bool]]):
        """Initialize a truth table with the names of variables and the logical function.
        Parameters
        ----------
        arg_names: list of strings
            names of arguments of the function
        out_names: list of strings
            names of outputs of the function (the function can have more than one output)
        """
        self._num_args = len(arg_names)

        data = np.full(shape=(2**self._num_args, len(out_names)), dtype=np.int8, fill_value=False)

        self._data = pd.DataFrame(columns=out_names, dtype=bool) # stores data

        self._names_to_nums = {name: num for num, name in enumerate(reversed(arg_names))} # map from names of arguments to numbers
        self._nums_to_names = {num: name for name, num in self._names_to_nums.items()} # reverse map

        for idx, args in enumerate(itertools.product([False, True], repeat=self._num_args)):
            self._data.loc[idx] = function(list(args))

    @staticmethod
    def _int_to_binary(integer: int, num_bits) -> List[bool]:
        """Convert to an integer to its binary representation.
        """
        binary_repr = []
        while integer != 0:
            integer, remainder = divmod(integer, 2)
            binary_repr.append(bool(remainder))

        while len(binary_repr) != num_bits:
            binary_repr.append(False)

        binary_repr.reverse()

        return binary_repr

    def get_value(self, args):
        idx = sum(2**(self._num_args-i-1) for i in range(self._num_args) if args[i])
        return self._data[idx]

    def predict_value(self, incomplete_args: Dict[str, bool]):
        """Given a dictionary that maps names of some of the arguments to their values, return:
        1. True or False if unspecified arguments are nonessential.
        2. None if missed arguments are essential.
        """
        incomplete_args = {key: val for key, val in incomplete_args.items() if val is not None}

        num_missed_args = self._num_args - len(incomplete_args)
        missed = []
        for name in self._names_to_nums:
            if name not in incomplete_args:
                missed.append(2**self._names_to_nums[name])

        return_if_cant_predict = {name: None for name in self._data.columns}

        first_index = sum(2**self._names_to_nums[i] for i in incomplete_args if incomplete_args[i])
        value = None
        for is_included in itertools.product([False, True], repeat=num_missed_args):
            cur_index = first_index + sum(missed[j] for j in range(num_missed_args) if is_included[j])
            cur_value = self._data.loc[cur_index]
            if value is None:
                value = cur_value
            elif np.any(value != cur_value):
                return return_if_cant_predict
        return dict(value)

    def __str__(self):
        str_repr = ""
        for num_row in range(self._data.shape[0]):
            cur_row = f"{num_row:0{self._num_args}b} "
            cur_row += str(list(self._data.loc[num_row]))
            str_repr += cur_row + "\n"
        return str_repr

    @classmethod
    def get_multiplexer_truth_table(cls, num_select_lines):
        def mux_func(lst_args):
            idx = 0
            for i in range(num_select_lines):
                idx += 2**i * lst_args[i]
            return [bool(lst_args[num_select_lines+idx])]
        args_names = [f"sel{i+1}" for i in range(num_select_lines)] + [f"in{i+1}" for i in range(2**num_select_lines)]
        outs_names = ['out']
        return cls(args_names, outs_names, mux_func)

    @classmethod
    def get_encoder_truth_table(cls, num_output_lines):
        def encoder_func(lst_args):
            out = [False] * num_output_lines
            for input_line in range(2**num_output_lines):
                if lst_args[input_line] == True:
                    binary = cls._int_to_binary(input_line, num_output_lines)
                    for idx, val in enumerate(binary[::-1]):
                        out[idx] = out[idx] or val
            return out
        args_names = [f"input line {i+1}" for i in range(2**num_output_lines)]
        outs_names = [f"output line {i+1}" for i in range(num_output_lines)]
        return cls(args_names, outs_names, encoder_func)

    @classmethod
    def get_decoder_truth_table(cls, num_input_lines):
        def decoder_func(lst_args):
            decoded = 0
            for input_line in range(num_input_lines):
                decoded += lst_args[input_line] * 2**input_line
            out = [False] * 2**num_input_lines
            out[decoded] = True
            return out
        args_names = [f"input line {i+1}" for i in range(num_input_lines)]
        outs_names = [f"output line {i+1}" for i in range(2**num_input_lines)]
        return cls(args_names, outs_names, decoder_func)

    @classmethod
    def get_fulladder_truth_table(cls):
        def fulladder_func(lst_args):
            bitA = lst_args[0]
            bitB = lst_args[1]
            carry_in = lst_args[2]
            return [(bitA != bitB) != carry_in,
                    (bitA and bitB) or (bitA and carry_in) or (bitB and carry_in)]

        return cls(['A', 'B', 'Cin'], ['S', 'Cout'], fulladder_func)

    @classmethod
    def get_addersubtractor_truth_table(cls, num_bits):
        def addersubtractor_func(lst_args):
            sub = lst_args[-1]
            number_A = lst_args[:num_bits]
            number_B = lst_args[num_bits: 2*num_bits]

            if sub:
                for idx, val in enumerate(number_B):
                    number_B[idx] = not number_B[idx]

            out = []
            carry = sub
            for i in range(num_bits):
                out.append((number_A[i] != number_B[i]) != carry)
                carry = (number_A[i] and number_B[i]) or (number_A[i] and carry) or (number_B[i] and carry)
            out.append(carry)
            return out

        args_names = [f'A{i}' for i in range(num_bits)]
        args_names.extend([f'B{i}' for i in range(num_bits)])
        args_names.append('sub')

        outs_names = [f'S{i}' for i in range(num_bits)]
        outs_names.append('Cout')

        return cls(args_names, outs_names, addersubtractor_func)

    @classmethod
    def get_rightshifter_truth_table(cls, num_bits):
        def rightshifter_func(lst_args):
            out = [False] * num_bits
            to_shift = lst_args[:num_bits]
            shift_by = lst_args[num_bits:]
            for i in range(num_bits):
                out[i] = False
                for j in range(i + 1):
                    out[i] = out[i] or (to_shift[i - j] and shift_by[j])
            return out
        args_names = [f'in{i}' for i in range(num_bits)]
        args_names.extend([f'shift_line{i}' for i in range(num_bits)])

        outs_names = [f'out{i}' for i in range(num_bits)]

        return cls(args_names, outs_names, rightshifter_func)

    @classmethod
    def get_gated_sr_flipflop_truth_table(cls):
        def sr_flipflop_func(set_, reset, prev_state):
            if not set_ and not reset:
                return [prev_state, prev_state]
            if not set_ and reset:
                return [False, False]
            if set_ and not reset:
                return [True, True]
            if set_ and reset:
                return [False, -1]

        def gated_sr_flipflop_func(lst_args):
            set_ = lst_args[0]
            reset = lst_args[1]
            enabled = lst_args[2]
            prev_state = lst_args[3]

            return sr_flipflop_func(set_ and enabled, reset and enabled, prev_state)

        return cls(['S', 'R', 'E', 'prev_state'], ['Q', 'next_state'], gated_sr_flipflop_func)

    @classmethod
    def get_gated_d_flipflop_truth_table(cls):
        def sr_flipflop_func(set_, reset, prev_state):
            if not set_ and not reset:
                return [prev_state, prev_state]
            if not set_ and reset:
                return [False, False]
            if set_ and not reset:
                return [True, True]
            if set_ and reset:
                return [False, -1]

        def gated_d_flipflop_func(lst_args):
            data = lst_args[0]
            enabled = lst_args[1]
            prev_state = lst_args[2]
            return sr_flipflop_func(data and enabled, not data and enabled, prev_state)

        return cls(['D', 'E', 'prev_state'], ['Q', 'next_state'], gated_d_flipflop_func)


if __name__ == "__main__":
    # print(TruthTable.get_decoder_truth_table(2))
    # print(TruthTable.get_decoder_truth_table(2).predict_value({'input line 1': False, 'input line 2': False}))
    print(TruthTable.get_gated_d_flipflop_truth_table())