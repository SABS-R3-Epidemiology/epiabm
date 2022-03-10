import unittest
import pandas as pd
import numpy as np
from enum import Enum

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

    def test_create__transition_time_matrix(self):
        """Tests the create_transition_time_matrix method by asserting that the matrix
        is of the right size and that the non-zero elements are of type
        InverseCdf."""
        matrix_object = TransitionTimeMatrix()
        matrix = matrix_object.create_transition_time_matrix()
        self.assertEqual(matrix.size, len(InfectionStatus)**2)
        for row in matrix.to_numpy():
            for element in row:
                if element != 0:
                    self.assertIsInstance(element,
                                          pe.utility.inverse_cdf.InverseCdf)

    def test_update_transition_time_with_float(self):
        # Test method updates transition time as expected
        matrix_object = TransitionTimeMatrix()
        row_status = InfectionStatus.Susceptible
        column_status = InfectionStatus.Exposed
        new_transition_time = 10.0
        transition_matrix = matrix_object.create_transition_time_matrix()
        matrix_object.update_transition_time_with_float(row_status,
                                                        column_status,
                                                        transition_matrix,
                                                        new_transition_time)
        self.assertEqual(10.0,
                         transition_matrix.loc['Susceptible', 'Exposed'])

        # Test error for incorrect columns is raised
        class TestInfectionStatus(Enum):
            Susceptiblesssss = 1

        with self.assertRaises(ValueError):
            row = TestInfectionStatus.Susceptiblesssss
            column = TestInfectionStatus.Susceptiblesssss
            matrix_object.update_transition_time_with_float(row, column,
                                                            transition_matrix,
                                                            1.0)

        with self.assertRaises(ValueError):
            row = None
            column = None
            matrix_object.update_transition_time_with_float(row, column,
                                                            transition_matrix,
                                                            1.0)

        # Test error for incorrect transition time is raised
        with self.assertRaises(ValueError):
            row = InfectionStatus.Susceptible
            column = InfectionStatus.Susceptible
            matrix_object.update_transition_time_with_float(row, column,
                                                            transition_matrix,
                                                            -5.0)

    def test_update_transition_time_with_icdf(self):
        # Test method updates transition time as expected
        matrix_object = TransitionTimeMatrix()
        row_status = InfectionStatus.Susceptible
        column_status = InfectionStatus.Exposed
        transition_time_icdf = np.ones(10)
        transition_time_icdf_mean = 10.0
        transition_matrix = matrix_object.create_transition_time_matrix()
        matrix_object.update_transition_time_with_icdf(
            row_status, column_status, transition_matrix,
            transition_time_icdf, transition_time_icdf_mean)
        test_updated_icdf = transition_matrix.loc['Susceptible', 'Exposed']
        self.assertEqual(10.0,
                         test_updated_icdf.mean)
        self.assertEqual((np.ones(10)).all(),
                         test_updated_icdf.icdf_array.all())

        # Test error for incorrect columns is raised
        class TestInfectionStatus(Enum):
            Susceptiblesssss = 1

        with self.assertRaises(ValueError):
            row = TestInfectionStatus.Susceptiblesssss
            column = TestInfectionStatus.Susceptiblesssss
            test_mean = 1.0
            test_icdf = np.ones(10)
            matrix_object.update_transition_time_with_icdf(
                row, column, transition_matrix,
                test_icdf, test_mean)

        with self.assertRaises(ValueError):
            row = None
            column = None
            test_mean = 1.0
            test_icdf = np.ones(10)
            matrix_object.update_transition_time_with_icdf(
                row, column, transition_matrix,
                test_icdf, test_mean)

        # Test error for incorrect icdf mean is raised
        with self.assertRaises(ValueError):
            row = InfectionStatus.Susceptible
            column = InfectionStatus.Susceptible
            test_mean = -5.0
            test_icdf = np.ones(10)
            matrix_object.update_transition_time_with_icdf(
                row, column, transition_matrix,
                test_icdf, test_mean)

        # Test error for incorrect size icdf array is raised
        with self.assertRaises(ValueError):
            row = InfectionStatus.Susceptible
            column = InfectionStatus.Susceptible
            test_mean = 1.0
            test_icdf = np.ones(1)
            matrix_object.update_transition_time_with_icdf(
                row, column, transition_matrix,
                test_icdf, test_mean)

        # Test error for negative icdf array valuesis raised
        with self.assertRaises(ValueError):
            row = InfectionStatus.Susceptible
            column = InfectionStatus.Susceptible
            test_mean = 1.0
            test_icdf = -1 * np.ones(10)
            matrix_object.update_transition_time_with_icdf(
                row,
                column,
                transition_matrix,
                test_icdf,
                test_mean)


if __name__ == '__main__':
    unittest.main()
