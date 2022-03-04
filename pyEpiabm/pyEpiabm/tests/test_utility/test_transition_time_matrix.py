import unittest

from pyEpiabm.utility import TransitionTimeMatrix
from pyEpiabm.utility import InverseCdf
import pandas as pd
import numpy as np


class TestTransitionTimeMatrix(unittest.TestCase):
    """Test the 'StateTransitionMatrix' class.
    """

    def test_fill_state_transition_matrix(self):
        matrix_object = TransitionTimeMatrix()
        matrix = matrix_object.fill_transition_time()
        print(matrix)
        icdf = matrix.loc['InfectASympt', 'Recovered']
        chosen_time = icdf.icdf_choose_noexp()
        print(chosen_time)


if __name__ == '__main__':
    unittest.main()
