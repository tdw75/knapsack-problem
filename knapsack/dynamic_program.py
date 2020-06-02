import time

import numpy as np

from knapsack.problem_setup import parse_input_data


def dp_solver(items, capacity):
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
    start = time.time()
    with open('..\data\ks_1000_0', 'r') as file:
        input_data = file.read()

    items, capacity = parse_input_data(input_data)
    solution, obj = dp_solver(items, capacity)

    print("best solution found was {}".format(obj))
    print("execution time = {:.1f} seconds".format(time.time() - start))
