import unittest

from pyEpiabm.utility import StateTransitionMatrix
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal


class TestStateTransitionMatrix(unittest.TestCase):
    """Test the 'StateTransitionMatrix' class.
    """
    def test_build_initial_matrix(self):
        """Tests the build_state_transition_matrix method by asserting if it is
        equal to the initial matrix expected.
        """
        matrix_object = StateTransitionMatrix()
        matrix = matrix_object.build_state_transition_matrix()
        labels = ['Susceptible', 'Exposed', 'InfectASympt', 'InfectMild',
                  'InfectGP', 'InfectHosp', 'InfectICU', 'InfectICURecov',
                  'Recovered', 'Dead']
        zero_filled_dataframe = pd.DataFrame(np.zeros((10, 10)),
                                             columns=labels, index=labels)
        print(zero_filled_dataframe.shape)
        assert_frame_equal(matrix, zero_filled_dataframe)

    def test_fill_state_transition_matrix(self):
        """Tests the fill_state_transition_matrix method and asserts that each row
        sums to 1 (ie that the transition probabilities for each current
        infection status sum to 1).
        """
        matrix_object = StateTransitionMatrix()
        matrix = matrix_object.build_state_transition_matrix()
        filled_matrix = matrix_object.fill_state_transition_matrix(matrix)
        print(filled_matrix)
        filled_matrix['sum'] = filled_matrix.sum(axis=1)
        for i in filled_matrix['sum']:
            self.assertAlmostEqual(i, 1)



if __name__ == '__main__':
    unittest.main()
