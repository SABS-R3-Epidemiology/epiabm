import unittest
import numpy as np
from enum import Enum

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import TransitionTimeMatrix
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestTransitionTimeMatrix(TestPyEpiabm):
    """Test the 'StateTransitionMatrix' class.
    """
    def test_create__transition_time_matrix(self):
        """Tests the create_transition_time_matrix method by asserting that the
        matrix is of the right size and that elements are of type InverseCdf
        (unless they are the default value of -1)."""
        matrix_object = TransitionTimeMatrix()
        matrix = matrix_object.matrix
        self.assertEqual(matrix.size, len(InfectionStatus)**2)
        for row in matrix.to_numpy():
            for element in row:
                with self.subTest(row=row, element=element):
                    if element != -1:
                        self.assertIsInstance(element,
                                              pe.utility.inverse_cdf.
                                              InverseCdf)

    def test_update_transition_time_with_float(self):
        # Test method updates transition time as expected
        matrix_object = TransitionTimeMatrix()
        row_status = InfectionStatus.Susceptible
        column_status = InfectionStatus.Exposed
        new_transition_time = 10.0
        transition_matrix = matrix_object.matrix
        matrix_object.update_transition_time_with_float(row_status,
                                                        column_status,
                                                        new_transition_time)
        self.assertEqual(10.0,
                         transition_matrix.loc['Susceptible', 'Exposed'])

        # Test error for incorrect columns is raised
        class TestInfectionStatus(Enum):
            Susceptiblesssss = 1

        with self.assertRaises(ValueError):
            row = TestInfectionStatus.Susceptiblesssss
            column = TestInfectionStatus.Susceptiblesssss
            matrix_object.update_transition_time_with_float(row, column, 1.0)

        with self.assertRaises(ValueError):
            row = None
            column = None
            matrix_object.update_transition_time_with_float(row, column, 1.0)

        # Test error for incorrect transition time is raised
        with self.assertRaises(ValueError):
            row = InfectionStatus.Susceptible
            column = InfectionStatus.Susceptible
            matrix_object.update_transition_time_with_float(row, column, -5.0)

    def test_update_transition_time_with_icdf(self):
        # Test method updates transition time as expected
        matrix_object = TransitionTimeMatrix()
        row_status = InfectionStatus.Susceptible
        column_status = InfectionStatus.Exposed
        transition_time_icdf = np.ones(10)
        transition_time_icdf_mean = 10.0
        transition_matrix = matrix_object.matrix
        matrix_object.update_transition_time_with_icdf(
            row_status, column_status, transition_time_icdf,
            transition_time_icdf_mean)
        test_updated_icdf = transition_matrix.loc['Susceptible', 'Exposed']
        self.assertEqual(10.0,
                         test_updated_icdf.mean)
        self.assertEqual((np.ones(10)).all(),
                         test_updated_icdf.icdf_array.all())

        # Test error for incorrect columns is raised
        class TestInfectionStatus(Enum):
            Susceptiblesssss = 1

        row = InfectionStatus.Susceptible
        column = InfectionStatus.Susceptible
        test_mean = 1.0
        test_icdf = np.ones(10)

        with self.assertRaises(ValueError):
            fake_row = TestInfectionStatus.Susceptiblesssss
            fake_column = TestInfectionStatus.Susceptiblesssss
            matrix_object.update_transition_time_with_icdf(
                fake_row, fake_column, test_icdf, test_mean)

        with self.assertRaises(ValueError):
            no_row = None
            no_column = None
            matrix_object.update_transition_time_with_icdf(
                no_row, no_column, test_icdf, test_mean)

        # Test error for incorrect icdf mean is raised
        with self.assertRaises(ValueError):
            negative_mean = -5.0
            matrix_object.update_transition_time_with_icdf(
                row, column, test_icdf, negative_mean)

        # Test error for incorrect size icdf array is raised
        with self.assertRaises(ValueError):
            short_icdf = np.ones(1)
            matrix_object.update_transition_time_with_icdf(
                row, column, short_icdf, test_mean)

        # Test error for negative icdf array valuesis raised
        with self.assertRaises(ValueError):
            neg_icdf = -1 * np.ones(10)
            matrix_object.update_transition_time_with_icdf(
                row, column, neg_icdf, test_mean)


if __name__ == '__main__':
    unittest.main()
