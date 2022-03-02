import unittest
from pyEpiabm.utility import StateTransitionMatrix

numReps = 1


class TestStateTransitionMatrix(unittest.TestCase):
    """Test the 'StateTransitionMatrix' class.
    """
    def test_build_initial_matrix(self):
        matrix_object = StateTransitionMatrix()
        matrix = matrix_object.build_state_transition_matrix()
        print(matrix)


if __name__ == '__main__':
    unittest.main()
