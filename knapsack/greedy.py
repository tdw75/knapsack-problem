from collections import namedtuple
from knapsack.problem_setup import parse_input_data, output_solution

Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])


def greedy_solver(items, capacity):
    obj_value = 0
    weight = 0
    decision_variables = [0] * len(items)

    items = sorted(items, key=lambda x: x.density, reverse=True)

    for item in items:
        if weight + item.weight <= capacity:
            decision_variables[item.index] = 1
            obj_value += item.value
            weight += item.weight

    return decision_variables, obj_value


def solve_it(input_data):

    items, capacity = parse_input_data(input_data)
    decision_variables, obj_value = greedy_solver(items, capacity)
    output_data = output_solution(decision_variables, obj_value)

    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()

        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python greedy.py ./data/ks_4_0)')
