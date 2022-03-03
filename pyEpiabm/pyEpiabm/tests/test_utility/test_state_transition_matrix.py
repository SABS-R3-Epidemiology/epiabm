import unittest
from pyEpiabm.utility import StateTransitionMatrix


class TestStateTransitionMatrix(unittest.TestCase):
    """Test the 'StateTransitionMatrix' class.
    """
    def test_build_initial_matrix(self):
        matrix_object = StateTransitionMatrix()
        matrix = matrix_object.build_state_transition_matrix()
        print(matrix)
        # Should test that elements are equal to 0?
        # Test dimensions?

    def test_fill_state_transition_matrix(self):
        matrix_object = StateTransitionMatrix()
        matrix = matrix_object.build_state_transition_matrix()
        matrix_object.fill_state_transition_matrix(matrix)
        print(matrix)
        # Test sum of rows = 1


if __name__ == '__main__':
    unittest.main()
