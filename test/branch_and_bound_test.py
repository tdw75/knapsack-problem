from unittest import TestCase

from branch_and_bound import BranchAndBound


class TestBranchAndBound(TestCase):

    def setUp(self) -> None:
        with open('resources\data\ks_4_0', 'r') as file:
            self.input_data = file.read()

    def test_that_relaxed_solution_with_no_variables_fixed_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data)
        fixed_vars = [None, None, None, None]
        solution = bnb.relaxed_solution(fixed_variables=fixed_vars)
        expected_solution = [0, 1, 1, 2 / 8]
        self.assertListEqual(expected_solution, solution)

    def test_that_relaxed_solution_with_some_variables_fixed_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data)
        fixed_vars = [None, 1, 0, None]
        solution = bnb.relaxed_solution(fixed_variables=fixed_vars)
        expected_solution = [0, 1, 0, 7 / 8]
        self.assertListEqual(expected_solution, solution)

    def test_that_relaxed_solution_with_all_variables_fixed_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data)
        fixed_vars = [1, 1, 0, 0]
        solution = bnb.relaxed_solution(fixed_variables=fixed_vars)
        self.assertListEqual(fixed_vars, solution)

    def test_that_infeasible_solution_returns_empty_list(self):
        bnb = BranchAndBound(self.input_data)
        fixed_vars = [1, 1, 0, 1]
        solution = bnb.relaxed_solution(fixed_variables=fixed_vars)
        self.assertListEqual([], solution)

    def test_that_feasible_solution_is_returned(self):
        bnb = BranchAndBound(self.input_data)
        feasible_solution = [1, 0, 0, 1]
        result = bnb.feasible(feasible_solution)
        self.assertEqual(result, True)

    def test_that_infeasible_solution_is_identified(self):
        bnb = BranchAndBound(self.input_data)
        infeasible_solution = [1, 1, 1, 0]
        result = bnb.feasible(infeasible_solution)
        self.assertEqual(result, False)

    def test_that_invalid_solution_is_identified(self):
        bnb = BranchAndBound(self.input_data)
        invalid_solution = [1, 0.25, 1, 0]
        result = bnb.valid(invalid_solution)
        self.assertEqual(result, False)

    def test_that_valid_solution_is_identified(self):
        bnb = BranchAndBound(self.input_data)
        valid_solution = [1, 1, 0, 0]
        result = bnb.valid(valid_solution)
        self.assertEqual(result, True)

    def test_that_objective_function_value_is_correctly_calculated(self):
        bnb = BranchAndBound(self.input_data)
        solution = [1, 0, 0, 1]
        value = bnb.calculate_objective_value(solution)
        expected = 19
        self.assertEqual(expected, value)

    def test_that_optimal_solution_is_found(self):
        bnb = BranchAndBound(self.input_data)
        solution, obj = bnb.solve()
        expected_solution = [1, 0, 0, 1]
        self.assertListEqual(expected_solution, solution)
        self.assertEqual(19, obj)
