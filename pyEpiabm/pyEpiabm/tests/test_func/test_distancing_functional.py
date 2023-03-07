import os
import pandas as pd
import unittest
from unittest.mock import patch, mock_open, Mock

import pyEpiabm as pe
from helper_func import HelperFunc


class TestDistancingFunctional(unittest.TestCase):
    """Functional testing of social distancing intervention. Conducts
    social distancing intervention simulations with known
    results/properties to ensure code functions as desired.
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestDistancingFunctional, cls).setUpClass()
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

    @classmethod
    def tearDownClass(cls):
        super(TestDistancingFunctional, cls).tearDownClass()
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
    def test_distancing_present(self, mock_read, mock_csv):
        """Social distancing functional test to ensure more people will be
        susceptible when social distancing intervention is present.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Without intervention
        pop = TestDistancingFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise()[1:])

        # Enable social distancing
        pe.Parameters.instance().intervention_params = self.intervention
        pop_distancing = TestDistancingFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().assert_greater_equal(
             pop.cells, pop_distancing.cells)

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_spatial_enhanced_large(self, mock_read, mock_csv):
        """Social distancing functional test to ensure less people will be
        susceptible when spatial enhanced susceptibility increases.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and social distancing
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestDistancingFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        self.intervention['social_distancing'][
            'distancing_spatial_enhanced_susc'] = 0.8
        pop = TestDistancingFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().assert_greater_equal(
             pop.cells, pop_standard.cells)

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_prob_lower(self, mock_read, mock_csv):
        """Social distancing functional test to ensure people within the
        age group of lower enhanced social distancing probability
        will have less susceptible individuals.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and social distancing
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestDistancingFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        self.intervention['social_distancing'][
            'distancing_enhanced_prob'] = [0.1]*17
        pop = TestDistancingFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().assert_greater_equal(
             pop.cells, pop_standard.cells)


if __name__ == '__main__':
    unittest.main()
