import pandas as pd
import unittest
from unittest.mock import patch, Mock

import pyEpiabm as pe
from pyEpiabm.tests import TestFunctional
from pyEpiabm.tests.test_func import HelperFunc


@patch('pyEpiabm.routine.simulation.tqdm', TestFunctional.notqdm)
@patch('pyEpiabm.output._CsvDictWriter.write', Mock())
@patch('os.makedirs', Mock())
@patch("pandas.DataFrame.to_csv")
@patch("pandas.read_csv")
class TestQuarantineFunctional(TestFunctional):
    """Functional testing of household quarantine intervention. Conducts
    household quarantine intervention simulations with known
    results/properties to ensure code functions as desired.
    """
    def setUp(self) -> None:
        TestFunctional.setUpPopulation()

        self.intervention = {"case_isolation": {
            "start_time": 0,
            "policy_duration": 365,
            "case_threshold": 0,
            "isolation_delay": 0,
            "isolation_duration": 3,
            "isolation_probability": 1,
            "isolation_effectiveness": 1,
            "isolation_house_effectiveness": 1},

            "household_quarantine": {
            "start_time": 0,
            "policy_duration": 365,
            "case_threshold": 0,
            "quarantine_delay": 0,
            "quarantine_duration": 10,
            "quarantine_house_compliant": 1.0,
            "quarantine_individual_compliant": 1.0,
            "quarantine_house_effectiveness": 1.1,
            "quarantine_spatial_effectiveness": 0.1,
            "quarantine_place_effectiveness": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        }
        }

    def test_quarantine_present(self, mock_read, mock_csv):
        """Household quarantine functional test to ensure more people will be
        susceptible when household quarantine intervention is present.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Enable case isolation
        pe.Parameters.instance().intervention_params = {
            "case_isolation": self.intervention['case_isolation']}
        pop_isolation = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        # Enable both case isolation and household quarantine
        pe.Parameters.instance().intervention_params = self.intervention
        pop_quarantine = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop_isolation.cells, pop_quarantine.cells)


if __name__ == '__main__':
    unittest.main()
