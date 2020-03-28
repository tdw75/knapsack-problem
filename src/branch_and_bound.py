import time
from typing import List, Tuple

import numpy as np

from src.problem_setup import parse_input_data


class BranchAndBound:
    def __init__(self, input_data, search_strategy='best_first'):
        self.items, self.capacity = parse_input_data(input_data)
        self.n = len(self.items)
        self.strategy = search_strategy
        self.sorted_items = sorted(self.items, key=lambda x: x.density, reverse=True)
        self.ranks = [item.index for item in self.sorted_items]
        self.ranks = np.argsort(self.ranks)
        self.decision_variables = None
        self.obj_value = None

    def relaxed_solution(self, fixed_variables: list = None) -> List[int]:

        decision_variables = fixed_variables.copy()
        items_stack = [self.sorted_items[idx] for idx in range(self.n) if
                       decision_variables[idx] is None]
        remaining_capacity = self.capacity - self.calculate_knapsack_weight(decision_variables)

        if remaining_capacity < 0:
            return []
        if not items_stack:
            return decision_variables

        for item in items_stack:
            if item.weight <= remaining_capacity:
                decision_variables[self.ranks[item.index]] = 1
                remaining_capacity -= item.weight
            else:
                decision_variables[self.ranks[item.index]] = remaining_capacity / item.weight
                break

        decision_variables = [x if x else 0 for x in decision_variables]

        return decision_variables

    @staticmethod
    def branch(index: int) -> List[Tuple[int, int]]:
        options = [(index, 0), (index, 1)]
        return options

    def bound(self, stack: List[tuple], current_config: List[int]) -> Tuple[int, List[int]]:
        current_idx = stack[-1][0]
        current_config = current_config[:current_idx] + [None] * (self.n - current_idx)
        return current_idx, current_config

    def feasible(self, decision_variables: List[int]) -> bool:
        weight = self.calculate_knapsack_weight(decision_variables)
        if weight <= self.capacity:
            return True
        else:
            return False

    @staticmethod
    def valid(decision_variables: List[int]) -> bool:
        for var in decision_variables:
            if 0 < 1 - var < 1:
                return False
        return True

    def calculate_objective_value(self, decision_variables: List[int]) -> bool:
        return sum([self.sorted_items[idx].value * decision_variables[idx] for idx in range(self.n) if
                    decision_variables[idx] is not None])

    def calculate_knapsack_weight(self, decision_variables):
        return sum([self.sorted_items[idx].weight * decision_variables[idx] for idx in range(self.n) if
                    decision_variables[idx] is not None])

    def best_so_far(self, current_best: int, decision_variables: List[int]) -> bool:
        value = self.calculate_objective_value(decision_variables)
        if value > current_best:
            return True
        else:
            return False

    def solve(self) -> Tuple[List[int], int]:
        best_obj = 0
        best_config = [0] * self.n
        current_idx = 0
        current_config = [None] * self.n
        stack = [(-1, 'placeholder')]
        stack += self.branch(0)
        next_up = stack.pop(-1)

        while stack:

            current_config[next_up[0]] = next_up[1]
            candidate_solution = self.relaxed_solution(current_config)

            if not candidate_solution:  # infeasible
                next_up = stack.pop(-1)

            elif self.best_so_far(best_obj, candidate_solution) and not self.valid(candidate_solution):
                current_idx += 1
                if current_idx >= self.n:
                    current_idx, current_config = self.bound(stack, current_config)
                    continue
                stack += self.branch(current_idx)
                next_up = stack.pop(-1)

            else:
                current_idx, current_config = self.bound(stack, current_config)
                next_up = stack.pop(-1)
                if self.best_so_far(best_obj, candidate_solution):
                    best_config = candidate_solution
                    best_obj = self.calculate_objective_value(best_config)

        item_indices = [item.index for item in self.sorted_items if best_config[self.ranks[item.index]] == 1]
        solution = [0] * self.n
        for idx in item_indices:
            solution[idx] = 1

        return solution, best_obj


if __name__ == "__main__":
    start = time.time()
    with open('..\data\ks_30_0', 'r') as file:
        input_data = file.read()

    bnb = BranchAndBound(input_data)
    configuration, obj = bnb.solve()

    print("best solution found was {}".format(obj))
    print("execution time = {:.2f} seconds".format(time.time() - start))
