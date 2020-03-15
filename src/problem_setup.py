from collections import namedtuple


def parse_input_data(input_data):
    Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])
    lines = input_data.split('\n')

    first_line = lines[0].split()
    item_count = int(first_line[0])
    capacity = int(first_line[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1]), int(parts[0]) / int(parts[1])))

    return items, capacity


def output_solution(decision_variables, obj_value, optimal=False):

    if optimal is True:
        opt = 1
    else:
        opt = 0

    output_data = str(obj_value) + ' ' + str(opt) + '\n'
    output_data += ' '.join(map(str, decision_variables))

    return output_data
