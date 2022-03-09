import unittest
import pandas as pd
import numpy as np

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.utility import TransitionTimeMatrix
from pandas.testing import assert_frame_equal


class TestTransitionTimeMatrix(unittest.TestCase):
    """Test the 'StateTransitionMatrix' class.
    """
    def test_build_initial_matrix(self):
        """Tests the __init__ method by asserting that the initial matrix that is
        built is equal to the initial matrix expected.
        """
        matrix_object = TransitionTimeMatrix()
        init_matrix = matrix_object.initial_matrix
        labels = [status.name for status in InfectionStatus]
        zero_filled_dataframe = pd.DataFrame(np.zeros((len(InfectionStatus),
                                             len(InfectionStatus))),
                                             columns=labels, index=labels)
        assert_frame_equal(init_matrix, zero_filled_dataframe)

    def test_fill_state_transition_matrix(self):
        """Tests the fill_state_transition method by asserting that the matrix
        is of the right size and that the non-zero elements are of type
        InverseCdf."""
        matrix_object = TransitionTimeMatrix()
        matrix = matrix_object.fill_transition_time()
        self.assertEqual(matrix.size, len(InfectionStatus)**2)
        for row in matrix.to_numpy():
            for element in row:
                if element != 0:
                    self.assertIsInstance(element,
                                          pe.utility.inverse_cdf.InverseCdf)


if __name__ == '__main__':
    unittest.main()
