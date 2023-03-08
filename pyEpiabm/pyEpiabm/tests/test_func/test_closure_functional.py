import os
import pandas as pd
import unittest
from unittest.mock import patch, mock_open, Mock

import pyEpiabm as pe

from helper_func import HelperFunc


class TestClosureFunctional(unittest.TestCase):
    """Functional testing of place closure intervention. Conducts
    place closure intervention simulations with known
    results/properties to ensure code functions as desired.
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestClosureFunctional, cls).setUpClass()
        cls.warning_patcher = patch('logging.warning')
        cls.error_patcher = patch('logging.error')

        cls.warning_patcher.start()
        cls.error_patcher.start()

        filepath = os.path.join(os.path.dirname(__file__),
                                os.pardir, 'testing_parameters.json')
        pe.Parameters.set_file(filepath)

    def setUp(self) -> None:
        self.pop_params = {'cell': [1.0, 2.0], 'microcell': [1.0, 1.0],
                           'location_x': [0.0, 1.0], 'location_y': [0.0, 1.0],
                           'household_number': [1, 1],
                           'Susceptible': [800, 900], 'InfectMild': [10, 0],
                           'place_number': 6}
        self.sim_params = {"simulation_start_time": 0,
                           "simulation_end_time": 15,
                           "initial_infected_number": 0}

        self.file_params = {"output_file": "output.csv",
                            "output_dir": "test_folder/integration_tests",
                            "spatial_output": False,
                            "age_stratified": True}

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

    @classmethod
    def tearDownClass(cls):
        super(TestClosureFunctional, cls).tearDownClass()
        cls.warning_patcher.stop()
        cls.error_patcher.stop()
        if pe.Parameters._instance:
            pe.Parameters._instance = None

    def notqdm(iterable, *args, **kwargs):
        """Replacement for tqdm that just passes back the iterable
        useful to silence `tqdm` in tests
        """
        return iterable

    def file_simulation(pop_file, sim_params, file_params, sweep_list):
        # Create a population based on the parameters given.
        population = pe.routine.FilePopulationFactory.make_pop(
            pop_file, random_seed=42)
        pe.routine.FilePopulationFactory.print_population(population,
                                                          "test.csv")

        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            sim = pe.routine.Simulation()
            sim.configure(
                population,
                [pe.sweep.InitialInfectedSweep(),
                 pe.sweep.InitialisePlaceSweep(),
                 pe.sweep.InitialHouseholdSweep()],
                sweep_list,
                sim_params,
                file_params)

            sim.run_sweeps()

        # Need to close the writer object at the end of each simulation.
        del sim.writer
        del sim
        return population

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_closure_present(self, mock_read, mock_csv):
        """Place closure functional test to ensure more people will be
        susceptible when place closure intervention is present.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Without intervention
        pop = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise()[1:])

        # Enable place closure
        pe.Parameters.instance().intervention_params = self.intervention
        pop_closure = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_closure.cells)

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
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
        pop = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise()[1:])

        pe.Parameters.instance().intervention_params = self.intervention
        self.intervention['place_closure']['closure_place_type'] = []
        pop_closure = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_closure.cells, method='equal')

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_closure_type_large(self, mock_read, mock_csv):
        """Place closure functional test to ensure more people will be
        susceptible when more types of places are closed.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and place closure
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['place_closure']['closure_place_type'] = [
            1, 2, 3, 4, 5, 6]
        pop = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop_standard.cells, pop.cells)

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
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
        pop_standard = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['place_closure'][
            'closure_spatial_params'] = 1
        pop = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_standard.cells)

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
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
        pop = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise()[1:])

        pe.Parameters.instance().intervention_params = self.intervention
        self.intervention['place_closure'][
            'case_microcell_threshold'] = 1000
        pop_closure = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_closure.cells, method='equal')

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_microcell_threshold_large(self, mock_read, mock_csv):
        """Place closure functional test to ensure fewer people will be
        susceptible when setting larger case threshold at microcell level.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and place closure
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        self.intervention['place_closure'][
            'case_microcell_threshold'] = 15
        pop = TestClosureFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc.sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().compare_susceptible_groups(
             pop.cells, pop_standard.cells)


if __name__ == '__main__':
    unittest.main()
