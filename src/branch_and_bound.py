from typing import List, Tuple

from src.problem_setup import parse_input_data


class BranchAndBound:
    def __init__(self, input_data):
        self.items, self.capacity = parse_input_data(input_data)
        self.n = len(self.items)
        self.sorted_items = sorted(self.items, key=lambda x: x.density, reverse=True)
        self.decision_variables = None
        self.obj_value = None

    def relaxed_solution(self, fixed_vars: dict = None) -> List[int]:
        decision_variables = [None] * self.n
        if fixed_vars:
            for k, v in fixed_vars.items():
                decision_variables[k] = v

        items = self.sorted_items
        remaining_capacity = self.capacity - sum(
            [self.items[idx].weight for idx in range(self.n) if decision_variables[idx] == 1])

        for item in items:
            if not decision_variables[item.index]:
                if item.weight <= remaining_capacity:
                    decision_variables[item.index] = 1
                    items.remove(item)
                    remaining_capacity -= item.weight

        decision_variables = [x if x else 0 for x in decision_variables]

        part_item = items[0]
        take = remaining_capacity / part_item.weight
        decision_variables[part_item.index] = take

        return decision_variables

    def branch(self, index: int, stack: list) -> List[Tuple[int, int]]:
        options = [(index, 1), (index, 0)]
        stack += options

        return stack

    def feasible(self, decision_variables: list) -> bool:
        weight = sum([self.items[idx].weight for idx in range(self.n) if decision_variables[idx] == 1])
        if weight <= self.capacity:
            return True
        else:
            return False

    def check_optimality(self, current_best: float, decision_variables: list) -> bool:
        value = sum([self.items[idx].value for idx in range(self.n) if decision_variables[idx] == 1])
        if value > current_best:
            return True
        else:
            return False

    def search(self):
        pass
