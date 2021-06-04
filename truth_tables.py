"""
truth_table.py

A module for implemetation of truth table and truth tables of logic elements.
"""

import ctypes
from typing import Dict, Callable


class TruthTable:
    """A class for the truth table of logical function.
    Methods
    -------
    get_value(vars)
        Given a list of boolean values, return the value that was calculated by the logical function.
    """
    def __init__(self, var_names: list, function: Callable):
        """Initialize a truth table with the names of variables and the logical function.
        """
        self._num_vars = len(var_names)
        self._data = (ctypes.py_object * 2**self._num_vars)() # stores data
        self._names_to_nums = {name: num for num, name in enumerate(var_names)} # map from names of variables to some numbers
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
        """Given a dictionary that maps some of the variables to their values, return:
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
            cur_row += str(int(self.get_value(vars_values)))
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


if __name__ == "__main__":
    print(TruthTable.get_multiplexer_truth_table(1))
