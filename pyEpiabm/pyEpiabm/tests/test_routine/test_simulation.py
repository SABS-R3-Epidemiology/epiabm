import os
import random
import numpy as np
import unittest
from unittest.mock import patch, mock_open

import pyEpiabm as pe


class TestSimulation(unittest.TestCase):
    """Tests the 'Simulation' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 0, "cell_number": 1,
                          "microcell_number": 1, "household_number": 1}
        cls.test_population = cls.pop_factory.make_pop(cls.pop_params)
        pe.Parameters.instance().time_steps_per_day = 1
        cls.sim_params = {"simulation_start_time": 0,
                          "simulation_end_time": 2,
                          "initial_infected_number": 0}

        cls.mock_output_dir = "pyEpiabm/pyEpiabm/tests/test_output/mock"
        cls.file_params = {"output_file": "test_file.csv",
                           "output_dir": cls.mock_output_dir}

        cls.spatial_file_params = dict(cls.file_params)
        cls.spatial_file_params["spatial_output"] = True

        cls.initial_sweeps = [pe.sweep.InitialInfectedSweep()]
        cls.sweeps = [pe.sweep.PlaceSweep()]

    def test_configure(self):
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):

            filename = os.path.join(os.getcwd(),
                                    self.file_params["output_dir"],
                                    self.file_params["output_file"])
            test_sim = pe.routine.Simulation()

            # Test configure binds parameters as expected.
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            self.assertEqual(len(test_sim.initial_sweeps), 1)
            self.assertEqual(len(test_sim.sweeps), 1)
            self.assertIsInstance(test_sim.population, pe.Population)
            del(test_sim.writer)
        mo.assert_called_with(filename, 'w')

    def test_spatial_output_bool(self):
        with patch('pyEpiabm.output._csv_dict_writer.open'):
            test_sim = pe.routine.Simulation()

            # Test default has no spatial output
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            self.assertFalse(test_sim.spatial_output)

            # Test that we can change spatial output to true
            spatial_sim = pe.routine.Simulation()
            spatial_sim.configure(self.test_population, self.initial_sweeps,
                                  self.sweeps, self.sim_params,
                                  self.spatial_file_params)
            self.assertTrue(spatial_sim.spatial_output)

            del(test_sim.writer)

    @patch('pyEpiabm.sweep.PlaceSweep.__call__')
    @patch('pyEpiabm.sweep.InitialInfectedSweep.__call__')
    @patch('pyEpiabm.routine.Simulation.write_to_file')
    def test_run_sweeps(self, patch_write, patch_initial, patch_sweep):
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):

            time_sweep = self.sim_params["simulation_start_time"] + 1
            time_write = self.sim_params["simulation_end_time"] - 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            test_sim.run_sweeps()
            patch_initial.assert_called_with(self.sim_params)
            patch_sweep.assert_called_with(time_sweep)
            patch_write.assert_called_with(time_write)

    def test_write_to_file(self):
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            data = {s: 0 for s in list(pe.property.InfectionStatus)}
            data["time"] = time

            with patch.object(test_sim.writer, 'write') as mock:
                test_sim.write_to_file(time)
                mock.assert_called_with(data)

    def test_s_write_to_file(self):
        # For spatial option to write to file
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            spatial_sim = pe.routine.Simulation()
            spatial_sim.configure(self.test_population, self.initial_sweeps,
                                  self.sweeps, self.sim_params,
                                  self.spatial_file_params)
            data = {s: 0 for s in list(pe.property.InfectionStatus)}
            data["time"] = time
            data["cell"] = hash(self.test_population.cells[0])

            with patch.object(spatial_sim.writer, 'write') as mock:
                spatial_sim.write_to_file(time)
                mock.assert_called_with(data)

    def test_set_random_seed(self):
        pe.routine.Simulation.set_random_seed(seed=0)
        value = random.random()
        np_value = np.random.random()
        self.assertAlmostEqual(value, 0.844422, places=5)
        self.assertAlmostEqual(np_value, 0.548814, places=5)
        # Values taken from known seed sequence

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
