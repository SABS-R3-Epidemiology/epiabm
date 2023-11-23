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
class TestIsolationFunctional(TestFunctional):
    """Functional testing of case isolation intervention. Conducts
    case isolation intervention simulations with known
    results/properties to ensure code functions as desired.
    """

    def setUp(self) -> None:
        TestFunctional.setUpPopulation()

        self.intervention = {"case_isolation": {
            "start_time": 0,
            "policy_duration": 365,
            "case_threshold": 0,
            "isolation_delay": 0,
            "isolation_duration": 12,
            "isolation_probability": 0.2,
            "use_testing": 0,
            "isolation_effectiveness": 0,
            "isolation_house_effectiveness": 0}
        }

    def test_isolation_present(self, mock_read, mock_csv):
        """Case isolation functional test to ensure more people will be
        susceptible when case isolation intervention is present.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Without intervention
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise()[1:])

        # Enable case isolation
        pe.Parameters.instance().intervention_params = self.intervention
        pop_isolation = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv',
                                     dtype={"cell": int,
                                            "microcell": int})
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_isolation.cells)

    def test_threshold_num(self, mock_read, mock_csv):
        """Case isolation functional test to ensure more people will be
        susceptible when the threshold of infectious individuals to start
        case isolation is less than the other.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and case isolation
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['case_isolation']['case_threshold'] = 20
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv',
                                     dtype={"cell": int,
                                            "microcell": int})
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_standard.cells)

    def test_delay_days(self, mock_read, mock_csv):
        """Case isolation functional test to ensure more people will be
        susceptible when the number of delay days is fewer than the other.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and case isolation
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        self.intervention['case_isolation']['isolation_delay'] = 10
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv',
                                     dtype={"cell": int,
                                            "microcell": int})
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_standard.cells)

    def test_duration_days(self, mock_read, mock_csv):
        """Case isolation functional test to ensure more people will be
        susceptible when the number of case isolation duration days is
        larger than the other.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and case isolation
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['case_isolation']['isolation_duration'] = 1
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv',
                                     dtype={"cell": int,
                                            "microcell": int})
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_standard.cells)

    def test_isolation_prob(self, mock_read, mock_csv):
        """Case isolation functional test to ensure fewer people will be
        susceptible when its isolation probability is less than the other.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and case isolation
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['case_isolation']['isolation_probability'] = 1
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv',
                                     dtype={"cell": int,
                                            "microcell": int})
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop_standard.cells, pop.cells)

    def test_isolation_effectiveness(self, mock_read, mock_csv):
        """Case isolation functional test to ensure more people will be
        susceptible when its isolation effectiveness is lower than the other.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and case isolation
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['case_isolation']['isolation_effectiveness'] = 0.5
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv',
                                     dtype={"cell": int,
                                            "microcell": int})
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_standard.cells)


if __name__ == '__main__':
    unittest.main()
