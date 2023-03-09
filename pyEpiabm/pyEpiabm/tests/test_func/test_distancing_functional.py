import pandas as pd
import unittest
from unittest.mock import patch, Mock

import pyEpiabm as pe
from pyEpiabm.tests import TestFunctional
from pyEpiabm.tests.test_func import HelperFunc


class TestDistancingFunctional(TestFunctional):
    """Functional testing of social distancing intervention. Conducts
    social distancing intervention simulations with known
    results/properties to ensure code functions as desired.
    """

    def setUp(self) -> None:
        TestFunctional.setUpPopulation()

        self.intervention = {"social_distancing": {
            "start_time": 0,
            "policy_duration": 365,
            "case_threshold": 0,
            "distancing_delay": 0,
            "distancing_duration": 12,
            "case_microcell_threshold": 0,
            "distancing_enhanced_prob": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                         1, 1, 1, 1, 1],
            "distancing_house_enhanced_susc": 0.2,
            "distancing_place_enhanced_susc": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
            "distancing_spatial_enhanced_susc": 0.2,
            "distancing_house_susc": 0.8,
            "distancing_place_susc": [0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
            "distancing_spatial_susc": 0.8
        }
        }

    @patch('pyEpiabm.routine.simulation.tqdm', TestFunctional.notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_distancing_present(self, mock_read, mock_csv):
        """Social distancing functional test to ensure more people will be
        susceptible when social distancing intervention is present.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Without intervention
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise()[1:])

        # Enable social distancing
        pe.Parameters.instance().intervention_params = self.intervention
        pop_distancing = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_distancing.cells)

    @patch('pyEpiabm.routine.simulation.tqdm', TestFunctional.notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_spatial_enhanced_large(self, mock_read, mock_csv):
        """Social distancing functional test to ensure fewer people will be
        susceptible when spatial enhanced susceptibility increases.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and social distancing
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['social_distancing'][
            'distancing_spatial_enhanced_susc'] = 0.8
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_standard.cells)

    @patch('pyEpiabm.routine.simulation.tqdm', TestFunctional.notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_prob_lower(self, mock_read, mock_csv):
        """Social distancing functional test to ensure people within the
        age group of lower enhanced social distancing probability
        will have fewer susceptible individuals.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and social distancing
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['social_distancing'][
            'distancing_enhanced_prob'] = [0.1]*17
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_standard.cells)


if __name__ == '__main__':
    unittest.main()
