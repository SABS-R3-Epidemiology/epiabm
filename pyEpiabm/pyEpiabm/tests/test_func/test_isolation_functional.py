import os
import pandas as pd
import unittest
from unittest.mock import patch, mock_open, Mock

import pyEpiabm as pe
from helper_func import HelperFunc


class TestIsolationFunctional(unittest.TestCase):
    """Functional testing of case isolation intervention. Conducts
    case isolation intervention simulations with known
    results/properties to ensure code functions as desired.
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestIsolationFunctional, cls).setUpClass()
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
                           'Susceptible': [800, 900], 'InfectMild': [10, 0]}
        self.sim_params = {"simulation_start_time": 0,
                           "simulation_end_time": 15,
                           "initial_infected_number": 0}

        self.file_params = {"output_file": "output.csv",
                            "output_dir": "test_folder/integration_tests",
                            "spatial_output": False,
                            "age_stratified": True}

        self.intervention = {"case_isolation": {
            "start_time": 0,
            "policy_duration": 365,
            "case_threshold": 0,
            "isolation_delay": 0,
            "isolation_duration": 12,
            "isolation_probability": 0.2,
            "isolation_effectiveness": 0,
            "isolation_house_effectiveness": 0}
        }

    @classmethod
    def tearDownClass(cls):
        super(TestIsolationFunctional, cls).tearDownClass()
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
    def test_isolation_present(self, mock_read, mock_csv):
        """Case isolation functional test to ensure more people will be
        susceptible when case isolation intervention is present.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Without intervention
        pop = TestIsolationFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise()[1:])

        # Enable case isolation
        pe.Parameters.instance().intervention_params = self.intervention
        pop_isolation = TestIsolationFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().assert_greater_equal(
             pop.cells, pop_isolation.cells)

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
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
        pop_standard = TestIsolationFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        self.intervention['case_isolation']['case_threshold'] = 20
        pop = TestIsolationFunctional.file_simulation(
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
    def test_delay_days(self, mock_read, mock_csv):
        """Case isolation functional test to ensure more people will be
        susceptible when the number of delay days is less than the other.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and case isolation
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestIsolationFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        self.intervention['case_isolation']['isolation_delay'] = 10
        pop = TestIsolationFunctional.file_simulation(
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
        pop_standard = TestIsolationFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        self.intervention['case_isolation']['isolation_duration'] = 1
        pop = TestIsolationFunctional.file_simulation(
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
    def test_isolation_prob(self, mock_read, mock_csv):
        """Case isolation functional test to ensure less people will be
        susceptible when its isolation probability is less than the other.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and case isolation
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestIsolationFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        self.intervention['case_isolation']['isolation_probability'] = 1
        pop = TestIsolationFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().assert_greater_equal(
             pop_standard.cells, pop.cells)

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write', Mock())
    @patch('os.makedirs', Mock())
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_isolation_effectiveness(self, mock_read, mock_csv):
        """Case isolation functional test to ensure more people will be
        susceptible when its isolation effectiveness is lower than the other.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious and case isolation
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        pe.Parameters.instance().intervention_params = self.intervention
        pop_standard = TestIsolationFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        self.intervention['case_isolation']['isolation_effectiveness'] = 0.5
        pop = TestIsolationFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params,
            HelperFunc().sweep_list_initialise())

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        # Compare number of susceptible individuals for each age group
        HelperFunc().assert_greater_equal(
             pop.cells, pop_standard.cells)


if __name__ == '__main__':
    unittest.main()
