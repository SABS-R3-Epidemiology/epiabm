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
class TestClosureFunctional(TestFunctional):
    """Functional testing of place closure intervention. Conducts
    place closure intervention simulations with known
    results/properties to ensure code functions as desired.
    """
    def setUp(self) -> None:
        TestFunctional.setUpPopulation()

        self.intervention = {"place_closure": {
            "start_time": 0,
            "policy_duration": 365,
            "case_threshold": 0,
            "closure_delay": 0,
            "closure_duration": 12,
            "closure_place_type": [1, 2, 3],
            "closure_household_infectiousness": 1.1,
            "closure_spatial_params": 0.2,
            "case_microcell_threshold": 0
        }
        }

    def test_closure_present(self, mock_read, mock_csv):
        """Place closure functional test to ensure more people will be
        susceptible when place closure intervention is present.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Without intervention
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise()[1:])

        # Enable place closure
        pe.Parameters.instance().intervention_params = self.intervention
        pop_closure = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv',
                                     dtype={"cell": int,
                                            "microcell": int})
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_closure.cells)

    def test_no_closure_type(self, mock_read, mock_csv):
        """Place closure functional test to ensure when no place
        closed type is specified, there is no effect of place closure
        intervention.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Without intervention
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise()[1:])

        pe.Parameters.instance().intervention_params = self.intervention
        self.intervention['place_closure']['closure_place_type'] = []
        pop_closure = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv',
                                     dtype={"cell": int,
                                            "microcell": int})
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_closure.cells, method='equal')

    def test_closure_type_large(self, mock_read, mock_csv):
        """Place closure functional test to ensure more people will be
        susceptible when more types of places are closed.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and place closure
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        self.intervention['place_closure']['closure_place_type'] = [6]
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['place_closure']['closure_place_type'] = [
            1, 2, 3, 4, 5, 6]
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

    def test_spatial_params_large(self, mock_read, mock_csv):
        """Place closure functional test to ensure fewer people will be
        susceptible when closure spatial params increases due to
        place closure.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and place closure
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['place_closure'][
            'closure_spatial_params'] = 1
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

    def test_microcell_threshold_extreme(self, mock_read, mock_csv):
        """Place closure functional test to ensure when the case
        threshold at microcell level exceeds the number of individuals,
        there is no effect of place closure
        intervention.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and place closure
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Without intervention
        pop = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise()[1:])

        pe.Parameters.instance().intervention_params = self.intervention
        self.intervention['place_closure'][
            'case_microcell_threshold'] = 1000
        pop_closure = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv',
                                     dtype={"cell": int,
                                            "microcell": int})
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_closure.cells, method='equal')

    def test_microcell_threshold_large(self, mock_read, mock_csv):
        """Place closure functional test to ensure fewer people will be
        susceptible when setting larger case threshold at microcell level.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and place closure
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['place_closure'][
            'case_microcell_threshold'] = 15
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
