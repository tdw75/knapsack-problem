from unittest import TestCase

from branch_and_bound import BranchAndBound
import numpy as np


class TestBranchAndBound(TestCase):

    def setUp(self) -> None:
        with open('data\ks_4_0_test', 'r') as file:
            self.input_data_4 = file.read()
        with open('data\ks_30_0_test', 'r') as file:
            self.input_data_30 = file.read()

    def test_that_relaxed_solution_with_no_variables_fixed_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data_4)
        fixed_vars = [np.nan, np.nan, np.nan, np.nan]
        solution = bnb.relaxed_solution(fixed_variables=np.array(fixed_vars))
        expected_solution = [1, 1, 2 / 8, 0]
        self.assertListEqual(expected_solution, list(solution))

    def test_that_relaxed_solution_with_some_variables_fixed_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data_4)
        fixed_vars = [1, 0, np.nan, np.nan]
        solution = bnb.relaxed_solution(fixed_variables=np.array(fixed_vars))
        expected_solution = [1, 0, 7 / 8, 0]
        self.assertEqual(expected_solution, list(solution))

    def test_that_relaxed_solution_with_all_variables_fixed_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data_4)
        fixed_vars = [1, 1, 0, 0]
        solution = bnb.relaxed_solution(fixed_variables=np.array(fixed_vars))
        self.assertListEqual(fixed_vars, list(solution))

    def test_that_infeasible_solution_returns_empty_array(self):
        bnb = BranchAndBound(self.input_data_4)
        fixed_vars = [1, 1, 0, 1]
        solution = bnb.relaxed_solution(fixed_variables=np.array(fixed_vars))
        self.assertListEqual([], list(solution))

    def test_that_feasible_solution_is_returned(self):
        bnb = BranchAndBound(self.input_data_4)
        feasible_solution = [1, 0, 0, 1]
        result = bnb.feasible(np.array(feasible_solution))
        self.assertEqual(result, True)

    def test_that_infeasible_solution_is_identified(self):
        bnb = BranchAndBound(self.input_data_4)
        infeasible_solution = [1, 1, 1, 0]
        result = bnb.feasible(np.array(infeasible_solution))
        self.assertEqual(result, False)

    def test_that_invalid_solution_is_identified(self):
        bnb = BranchAndBound(self.input_data_4)
        invalid_solution = [1, 0.25, 1, 0]
        result = bnb.valid(np.array(invalid_solution))
        self.assertEqual(result, False)

    def test_that_valid_solution_is_identified(self):
        bnb = BranchAndBound(self.input_data_4)
        valid_solution = [1, 1, 0, 0]
        result = bnb.valid(np.array(valid_solution))
        self.assertEqual(result, True)

    def test_that_objective_function_value_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data_4)
        solution = [0, 0, 1, 1]
        value = bnb.calculate_objective_value(np.array(solution))
        expected = 19
        self.assertEqual(expected, value)

    def test_that_knapsack_weight_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data_4)
        knapsack = [0, 1, 1, np.nan]
        weight = bnb.calculate_knapsack_weight(np.array(knapsack))
        self.assertEqual(13, weight)

    def test_that_optimal_solution_is_found(self):
        bnb = BranchAndBound(self.input_data_4)
        solution, obj = bnb.solve()
        expected_solution = [1, 0, 0, 1]
        self.assertEqual(19, obj)
        self.assertListEqual(expected_solution, solution)

    def test_that_optimal_solution_is_found_large(self):
        bnb = BranchAndBound(self.input_data_30)
        solution, obj = bnb.solve()
        self.assertEqual(99798, obj)
