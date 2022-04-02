import os
import unittest
from unittest.mock import patch, mock_open

import pyEpiabm as pe


class TestPopulationRandomSeeds(unittest.TestCase):
    """Test random seed usage in population generation
    """
    def test_placeholder(self):
        self.assertEqual(2, 1+1)


class TestSimulationRandomSeeds(unittest.TestCase):
    """Test random seed usage in simulation evaluation
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestSimulationRandomSeeds, cls).setUpClass()

        cls.warning_patcher = patch('logging.warning')
        cls.error_patcher = patch('logging.error')
        cls.warning_patcher.start()
        cls.error_patcher.start()

        filepath = os.path.join(os.path.dirname(__file__),
                                os.pardir, 'testing_parameters.json')
        pe.Parameters.set_file(filepath)

        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 0, "cell_number": 1,
                          "microcell_number": 1, "household_number": 1}
        cls.test_population = cls.pop_factory.make_pop(cls.pop_params)
        pe.Parameters.instance().time_steps_per_day = 1
        cls.sim_params = {"simulation_start_time": 0,
                          "simulation_end_time": 1,
                          "initial_infected_number": 0}

        cls.mock_output_dir = "pyEpiabm/pyEpiabm/tests/test_output/mock"
        cls.file_params = {"output_file": "test_file.csv",
                           "output_dir": cls.mock_output_dir}

        cls.spatial_file_params = dict(cls.file_params)
        cls.spatial_file_params["spatial_output"] = True

        cls.initial_sweeps = [pe.sweep.InitialInfectedSweep()]
        cls.sweeps = [pe.sweep.PlaceSweep()]

    @classmethod
    def tearDownClass(cls):
        """Inherits from the unittest teardown, and remove all patches"""
        super(TestSimulationRandomSeeds, cls).tearDownClass()
        cls.warning_patcher.stop()
        cls.error_patcher.stop()

    def notqdm(iterable, *args, **kwargs):
        """Replacement for tqdm that just passes back the iterable
        useful to silence `tqdm` in tests
        """
        return iterable

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write')
    def test_random_seed(self, mock_write):
        pop_params = {"population_size": 250, "cell_number": 1,
                      "microcell_number": 1, "household_number": 5,
                      "population_seed": 42}
        pe.Parameters.instance().time_steps_per_day = 1
        sim_params = {"simulation_start_time": 0,
                      "simulation_end_time": 10,
                      "initial_infected_number": 20,
                      "simulation_seed": 42}

        # Care has been taken in setting the end time of the simulation
        # to ensure that partial infection is achieved across the population,
        # so that different seeds will result in a unique final state

        initial_sweeps = [pe.sweep.InitialInfectedSweep()]
        sim_sweeps = [pe.sweep.UpdatePlaceSweep(), pe.sweep.HouseholdSweep(),
                      pe.sweep.PlaceSweep(), pe.sweep.QueueSweep(),
                      pe.sweep.HostProgressionSweep()]

        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            seed_pop = self.pop_factory.make_pop(pop_params)
            seed_sim = pe.routine.Simulation()
            seed_sim.configure(seed_pop, initial_sweeps, sim_sweeps,
                               sim_params, self.file_params)
            seed_sim.run_sweeps()
        seed_output = mock_write.call_args

        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            comp_pop = self.pop_factory.make_pop(pop_params)
            comp_sim = pe.routine.Simulation()
            comp_sim.configure(comp_pop, initial_sweeps, sim_sweeps,
                               sim_params, self.file_params)
            comp_sim.run_sweeps()
        comp_output = mock_write.call_args

        sim_params["simulation_seed"] = 43  # Change seed of population
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            diff_pop = self.pop_factory.make_pop(pop_params)
            diff_sim = pe.routine.Simulation()
            diff_sim.configure(diff_pop, initial_sweeps, sim_sweeps,
                               sim_params, self.file_params)
            diff_sim.run_sweeps()
        diff_output = mock_write.call_args

        self.assertEqual(seed_output, comp_output)
        self.assertNotEqual(seed_output, diff_output)


if __name__ == '__main__':
    unittest.main()
