import numpy as np
from problem_setup import parse_input_data, output_solution


def dynamic_program(items, capacity):
    dp_table = {}
    n = len(items)
    columns = n + 1

    for i in range(columns):
        dp_table[i] = [0] * (capacity + 1)

    for col in range(1, columns):

        j = col - 1

        for k in range(capacity + 1):

            if items[j].weight <= k:
                dp_table[col][k] = max(dp_table[col - 1][k], items[j].value + dp_table[col - 1][k - items[j].weight])
            else:
                dp_table[col][k] = dp_table[col - 1][k]

    obj_value = dp_table[n][capacity]
    decision_variables = [np.nan] * n
    row = capacity
    column_list = list(dp_table.keys())

    for i in column_list[:0:-1]:
        if dp_table[i][row] != dp_table[i - 1][row]:
            decision_variables[i - 1] = 1
            row = row - items[i - 1].weight
        else:
            decision_variables[i - 1] = 0

    return decision_variables, obj_value


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:

        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()

        items, capacity = parse_input_data(input_data)
        decision_variables, obj_value = dynamic_program(items, capacity)
        print(output_solution(decision_variables, obj_value))

    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python dp.py ./data/ks_4_0)')
