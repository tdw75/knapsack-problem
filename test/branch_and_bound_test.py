from unittest import TestCase

from branch_and_bound import BranchAndBound


class TestBranchAndBound(TestCase):

    def setUp(self) -> None:
        with open('resources\data\ks_test', 'r') as file:
            self.input_data = file.read()

    def test_that_relaxed_solution_with_fixed_variables_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data)
        fixed_vars = {1: 1}
        solution = bnb.relaxed_solution(fixed_vars=fixed_vars)
        expected_solution = [0, 1, 1]
        self.assertListEqual(expected_solution, solution)

    def test_that_relaxed_solution_without_fixed_variables_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data)
        solution = bnb.relaxed_solution(fixed_vars=None)
        expected_solution = [1, 0.5, 0]
        self.assertListEqual(expected_solution, solution)

    def test_that_feasible_solution_is_returned(self):
        bnb = BranchAndBound(self.input_data)
        solution_feasible = [0, 1, 1]
        result_feasible = bnb.feasible(solution_feasible)
        self.assertEqual(result_feasible, True)

    def test_that_infeasible_solution_is_identified(self):
        bnb = BranchAndBound(self.input_data)
        solution_infeasible = [1, 0, 1]
        result_infeasible = bnb.feasible(solution_infeasible)
        self.assertEqual(result_infeasible, False)
