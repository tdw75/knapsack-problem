import time
from typing import List, Tuple

from src.problem_setup import parse_input_data


class BranchAndBound:
    def __init__(self, input_data):
        self.items, self.capacity = parse_input_data(input_data)
        self.n = len(self.items)
        self.sorted_items = sorted(self.items, key=lambda x: x.density, reverse=True)
        self.decision_variables = None
        self.obj_value = None

    def relaxed_solution(self, fixed_variables: list = None) -> List[int]:

        decision_variables = fixed_variables.copy()
        items_stack = [self.sorted_items[idx] for idx in range(self.n) if
                       decision_variables[self.sorted_items[idx].index] is None]
        remaining_capacity = self.capacity - self.calculate_knapsack_weight(decision_variables)

        if remaining_capacity < 0:
            return []
        if not items_stack:
            return decision_variables

        for item in items_stack:
            # if not decision_variables[item.index]:
            if item.weight <= remaining_capacity:
                decision_variables[item.index] = 1
                remaining_capacity -= item.weight
            else:
                decision_variables[item.index] = remaining_capacity / item.weight
                break

        decision_variables = [x if x else 0 for x in decision_variables]

        return decision_variables

    @staticmethod
    def branch(index: int) -> List[Tuple[int, int]]:
        options = [(index, 0), (index, 1)]
        return options

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
        return sum([self.items[idx].value for idx in range(self.n) if decision_variables[idx] == 1])

    def calculate_knapsack_weight(self, decision_variables):
        return sum([self.items[idx].weight for idx in range(self.n) if decision_variables[idx] == 1])

    def best_so_far(self, current_best: int, decision_variables: List[int]) -> bool:
        value = self.calculate_objective_value(decision_variables)
        if value > current_best:
            return True
        else:
            return False

    def solve(self):
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

            elif self.feasible(candidate_solution) and not self.valid(candidate_solution):
                current_idx += 1
                if current_idx >= self.n:
                    current_idx = stack[-1][0]
                    continue
                stack += self.branch(current_idx)
                next_up = stack.pop(-1)

            elif self.valid(candidate_solution):
                current_idx = stack[-1][0]
                current_config = current_config[:current_idx] + [None] * (self.n - current_idx)
                next_up = stack.pop(-1)
                if self.best_so_far(best_obj, candidate_solution):
                    best_config = candidate_solution
                    best_obj = self.calculate_objective_value(best_config)

        # item_indices = [item.index for item in self.items if best_config[item.index] == 1]
        item_indices = [item.index for item in self.items if best_config[item.index] == 1]
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
    print("execution time = {:.1f} seconds".format(time.time() - start))
