import time
from typing import List, Tuple

import numpy as np

from src.problem_setup import parse_input_data


class BranchAndBound:
    def __init__(self, input_data):
        self.items, self.capacity = parse_input_data(input_data)
        self.n = len(self.items)
        self.ranked_items = np.array(sorted(self.items, key=lambda x: x.density, reverse=True))
        self.ranked_indices = self.ranked_items[:, 0]
        self.ranked_values = self.ranked_items[:, 1]
        self.ranked_weights = self.ranked_items[:, 2]
        self.ranks = np.argsort(self.ranked_indices)
        self.decision_variables = None
        self.obj_value = None

    def relaxed_solution(self, fixed_variables: np.array) -> np.array:

        decision_variables = fixed_variables.copy()
        indices = np.isnan(decision_variables)
        items_stack = self.ranked_items[indices]
        remaining_capacity = self.capacity - self.calculate_knapsack_weight(decision_variables)

        if remaining_capacity < 0:
            return np.array([])

        for item in items_stack:

            if item[2] <= remaining_capacity:
                decision_variables[self.ranks[int(item[0])]] = 1
                remaining_capacity -= item[2]
            else:
                decision_variables[self.ranks[int(item[0])]] = remaining_capacity / item[2]
                break

        decision_variables = np.where(np.isnan(decision_variables), 0, decision_variables)

        return decision_variables

    @staticmethod
    def branch(index: int) -> List[Tuple[int, int]]:
        options = [(index, 0), (index, 1)]
        return options

    def bound(self, stack: List[tuple], current_config: np.ndarray) -> Tuple[int, np.ndarray]:
        current_idx = stack[-1][0]
        current_config = np.append(current_config[:current_idx], [np.nan] * (self.n - current_idx))
        return current_idx, current_config

    def feasible(self, decision_variables: np.ndarray) -> bool:
        weight = self.calculate_knapsack_weight(decision_variables)
        if weight <= self.capacity:
            return True
        else:
            return False

    @staticmethod
    def valid(decision_variables: np.ndarray) -> bool:
        for var in decision_variables:
            if 0 < 1 - var < 1:
                return False
        return True

    def calculate_objective_value(self, decision_variables: np.ndarray) -> int:
        product = self.ranked_values * decision_variables
        return product.sum()

    def calculate_knapsack_weight(self, decision_variables: np.ndarray) -> int:
        product = self.ranked_weights * decision_variables
        product = product[~np.isnan(product)]
        return product.sum()

    def best_so_far(self, current_best: int, decision_variables: np.array) -> bool:
        value = self.calculate_objective_value(decision_variables)
        if value > current_best:
            return True
        else:
            return False

    def solve(self) -> Tuple[List[int], int]:
        best_obj = 0
        best_config = [0] * self.n
        current_idx = 0
        current_config = [np.nan] * self.n
        current_config = np.array(current_config)
        stack = [(-1, 'placeholder')]
        stack += self.branch(0)
        next_up = stack.pop(-1)

        while stack:

            current_config[next_up[0]] = next_up[1]
            candidate_solution = self.relaxed_solution(current_config)

            # infeasible solution
            if candidate_solution.size == 0:
                current_idx, current_config = self.bound(stack, current_config)
                next_up = stack.pop(-1)

            # feasible but invalid solution
            elif self.best_so_far(best_obj, candidate_solution) and not self.valid(candidate_solution):
                current_idx += 1
                if current_idx >= self.n:
                    current_idx, current_config = self.bound(stack, current_config)
                    continue
                stack += self.branch(current_idx)
                next_up = stack.pop(-1)

            # feasible and valid solution
            else:
                current_idx, current_config = self.bound(stack, current_config)
                next_up = stack.pop(-1)
                if self.best_so_far(best_obj, candidate_solution):
                    best_config = candidate_solution
                    best_obj = self.calculate_objective_value(best_config)

        item_indices = [int(item[0]) for item in self.ranked_items if best_config[self.ranks[int(item[0])]] == 1]
        solution = [0] * self.n
        for idx in item_indices:
            solution[idx] = 1

        return solution, int(best_obj)


if __name__ == "__main__":
    start = time.time()
    with open('..\data\ks_30_0', 'r') as file:
        input_data = file.read()

    bnb = BranchAndBound(input_data)
    configuration, obj = bnb.solve()

    print("best solution found was {}".format(obj))
    print("execution time = {:.2f} seconds".format(time.time() - start))
