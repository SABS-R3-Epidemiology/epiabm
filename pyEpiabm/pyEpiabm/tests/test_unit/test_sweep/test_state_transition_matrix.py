from collections import defaultdict
from enum import Enum
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import unittest
from unittest import mock

from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import StateTransitionMatrix
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestStateTransitionMatrix(TestPyEpiabm):
    """Test the 'StateTransitionMatrix' class.
    """

    def setUp(self) -> None:
        self.empty_coefficients = defaultdict(int)
        self.matrix_object = StateTransitionMatrix(self.empty_coefficients)

        self.real_coefficients = {
            "prob_exposed_to_asympt": 0.4,
            "prob_exposed_to_mild": 0.4,
            "prob_exposed_to_gp": 0.2,
            "prob_gp_to_recov": 0.9,
            "prob_gp_to_hosp": 0.1,
            "prob_hosp_to_recov": 0.6,
            "prob_hosp_to_icu": 0.2,
            "prob_hosp_to_death": 0.2,
            "prob_icu_to_icurecov": 0.5,
            "prob_icu_to_death": 0.5
        }

        self.list_coefficients = defaultdict(
            int, {
                "prob_exposed_to_asympt": [0.8, 0.2],
                "prob_exposed_to_mild": [0.2, 0.8],
            }
        )
        self.age_prop = [0.1, 0.9]

    def test_init(self):
        self.assertIsInstance(self.matrix_object.matrix, pd.DataFrame)
        self.assertFalse(self.matrix_object.age_dependent)
        self.matrix_object_ad = StateTransitionMatrix(self.empty_coefficients,
                                                      use_ages=True)
        self.assertTrue(self.matrix_object_ad.age_dependent)

    def test_create_empty_transition_matrix(self):
        """Tests the build_state_transition_matrix method by asserting if it is
        equal to the initial matrix expected.
        """
        empty_mat = self.matrix_object.create_empty_state_transition_matrix()
        labels = [status.name for status in InfectionStatus]
        zero_filled_dataframe = pd.DataFrame(np.zeros((len(InfectionStatus),
                                                       len(InfectionStatus))),
                                             columns=labels, index=labels,
                                             dtype='object')
        assert_frame_equal(empty_mat, zero_filled_dataframe)

    def test_create_state_transition_matrix(self):
        """Tests the fill_state_transition_matrix method and asserts that
        each row sums to 1 (ie that the transition probabilities for each
        current infection status sum to 1).
        """
        filled_matrix = StateTransitionMatrix(self.real_coefficients)
        row_sums = filled_matrix.matrix.sum(axis=1)
        for i in row_sums:
            self.assertAlmostEqual(i, 1)

    def test_create_state_transition_matrix_waning_immunity(self):
        """Tests that we have a Recovered to Susceptible probability with
        waning immunity turned on, and that we have not broken summing to 1
        """
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value.use_waning_immunity = 1.0
            waning_matrix = StateTransitionMatrix(self.real_coefficients)
            self.assertEqual(waning_matrix.matrix.loc['Recovered',
                                                      'Susceptible'], 1.0)
            self.assertEqual(waning_matrix.matrix.loc['Recovered',
                                                      'Recovered'], 0.0)
            row_sums = waning_matrix.matrix.sum(axis=1)
            for i in row_sums:
                self.assertAlmostEqual(i, 1)

    def test_update_probability(self):
        # Test method updates probability as expected
        row_status = InfectionStatus.Susceptible
        column_status = InfectionStatus.Exposed
        new_probability = 0.5
        transition_matrix = self.matrix_object.matrix
        self.matrix_object.update_probability(row_status, column_status,
                                              new_probability)
        self.assertEqual(0.5,
                         transition_matrix.loc['Susceptible', 'Exposed'])

        # Test error for incorrect columns is raised
        class TestInfectionStatus(Enum):
            Susceptiblesssss = 1

        with self.assertRaises(ValueError):
            row = TestInfectionStatus.Susceptiblesssss
            column = TestInfectionStatus.Susceptiblesssss
            self.matrix_object.update_probability(row, column, 0.5)

        with self.assertRaises(ValueError):
            row = None
            column = None
            self.matrix_object.update_probability(row, column, 0.5)

        # Test error for incorrect probability is raised
        with self.assertRaises(ValueError):
            row = InfectionStatus.Susceptible
            column = InfectionStatus.Susceptible
            self.matrix_object.update_probability(row, column, 10.0)

    def test_age_dependance(self):
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value.age_proportions = self.age_prop
            matrix_object = StateTransitionMatrix(self.list_coefficients,
                                                  use_ages=True)
            mock_param.assert_not_called
            output = matrix_object.matrix
            self.assertListEqual([0.8, 0.2], output.loc['Exposed',
                                                        'InfectASympt'])
            self.assertEqual([0.2, 0.8], output.loc['Exposed', 'InfectMild'])

    def test_remove_age_dependance(self):
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value.age_proportions = self.age_prop
            matrix_object = StateTransitionMatrix(self.list_coefficients,
                                                  use_ages=False)
            mock_param.assert_called_once
            output = matrix_object.matrix
            self.assertAlmostEqual(0.26, output.loc['Exposed', 'InfectASympt'])
            self.assertAlmostEqual(0.74, output.loc['Exposed', 'InfectMild'])


if __name__ == '__main__':
    unittest.main()
