import os
import random
import numpy as np
import unittest
from unittest.mock import patch, mock_open

import pyEpiabm as pe

from pyEpiabm.tests.test_unit.mocked_logging_tests import TestMockedLogs


class TestSimulation(TestMockedLogs):
    """Tests the 'Simulation' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestSimulation, cls).setUpClass()  # Sets up patch on logging
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
        cls.ih_file_params = {"output_dir": cls.mock_output_dir,
                              "status_output": False,
                              "infectiousness_output": False}
        cls.spatial_file_params = dict(cls.file_params)
        cls.spatial_file_params["age_stratified"] = True
        cls.spatial_file_params["spatial_output"] = True

        cls.initial_sweeps = [pe.sweep.InitialInfectedSweep()]
        cls.sweeps = [pe.sweep.PlaceSweep()]

    def notqdm(iterable, *args, **kwargs):
        """Replacement for tqdm that just passes back the iterable
        useful to silence `tqdm` in tests
        """
        return iterable

    @patch('os.makedirs')
    def test_configure(self, mock_mkdir):
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

            # Test that the ih writers are None, as both status_output
            # and infectiousness_output are False
            self.assertEqual(test_sim.ih_status_writer, None)
            self.assertEqual(test_sim.ih_infectiousness_writer, None)

            del test_sim.writer
            del test_sim.ih_status_writer
            del test_sim.ih_infectiousness_writer
        mo.assert_called_with(filename, 'w')

    @patch('os.makedirs')
    def test_configure_ih_status(self, mock_mkdir):
        mo = mock_open()
        self.ih_file_params["infectiousness_output"] = False
        self.ih_file_params["status_output"] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):

            filename = os.path.join(os.getcwd(),
                                    self.ih_file_params["output_dir"],
                                    "ih_status_output.csv")
            test_sim = pe.routine.Simulation()

            # Test that the output titles are correct
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.ih_file_params)

            self.assertEqual(test_sim.ih_output_titles, ["time"])
            # Test that the ih_infectiousness_writer is None, as
            # infectiousness_output is False
            self.assertEqual(test_sim.ih_infectiousness_writer, None)

            del test_sim.writer
            del test_sim.ih_status_writer
            del test_sim.ih_infectiousness_writer
        mo.assert_called_with(filename, 'w')

    @patch('os.makedirs')
    def test_configure_ih_infectiousness(self, mock_mkdir):
        mo = mock_open()
        self.ih_file_params["infectiousness_output"] = True
        self.ih_file_params["status_output"] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):

            filename = os.path.join(os.getcwd(),
                                    self.ih_file_params["output_dir"],
                                    "ih_infectiousness_output.csv")
            test_sim = pe.routine.Simulation()

            # Test that the output titles are correct
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.ih_file_params)

            self.assertEqual(test_sim.ih_output_titles, ["time"])
            # Test that the ih_status_writer is None, as
            # infectiousness_output is False
            self.assertEqual(test_sim.ih_status_writer, None)

            del test_sim.writer
            del test_sim.ih_status_writer
            del test_sim.ih_infectiousness_writer
        mo.assert_called_with(filename, 'w')

    @patch('logging.exception')
    @patch('os.path.join')
    def test_configure_exception(self, mock_join, mock_log):
        mock_join.side_effect = SyntaxError
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            mock_log.assert_called_once_with("SyntaxError in"
                                             + " Simulation.configure()")

    @patch('os.makedirs')
    def test_spatial_output_bool(self, mock_mkdir):
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
            self.assertTrue(spatial_sim.age_stratified)

            del test_sim.writer
            self.assertEqual(mock_mkdir.call_count, 2)
            mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                          self.file_params["output_dir"]))

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.sweep.PlaceSweep.__call__')
    @patch('pyEpiabm.sweep.InitialInfectedSweep.__call__')
    @patch('pyEpiabm.routine.Simulation.write_to_file')
    @patch('os.makedirs')
    def test_run_sweeps(self, mock_mkdir, patch_write, patch_initial,
                        patch_sweep):
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):

            time_sweep = self.sim_params["simulation_start_time"] + 1
            time_write = self.sim_params["simulation_end_time"]
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            test_sim.run_sweeps()
            patch_initial.assert_called_with(self.sim_params)
            patch_sweep.assert_called_with(time_sweep)
            patch_write.assert_called_with(time_write)

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.sweep.PlaceSweep.__call__')
    @patch('pyEpiabm.sweep.InitialInfectedSweep.__call__')
    @patch('pyEpiabm.routine.Simulation.write_to_file')
    @patch('os.makedirs')
    def test_run_sweeps_with_writer(
            self, mock_mkdir, patch_write, patch_initial, patch_sweep):
        if os.path.exists(self.file_params["output_dir"]):
            os.rmdir(self.file_params["output_dir"])

        mo = mock_open()
        mo2 = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo), \
             patch('pyEpiabm.output._csv_writer.open', mo2):

            time_sweep = self.sim_params["simulation_start_time"] + 1
            time_write = self.sim_params["simulation_end_time"]
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            test_sim.add_writer(
                pe.output.NewCasesWriter(
                    os.path.join(os.getcwd(), self.file_params["output_dir"])))
            test_sim.run_sweeps()
            patch_initial.assert_called_with(self.sim_params)
            patch_sweep.assert_called_with(time_sweep)
            patch_write.assert_called_with(time_write)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.file_params["output_dir"]))

    @patch('os.makedirs')
    @patch('logging.exception')
    @patch('pyEpiabm.sweep.InitialInfectedSweep.__call__')
    def test_run_sweeps_exception(self, patch_initial, patch_log, mock_mkdir):
        patch_initial.side_effect = NotImplementedError

        if os.path.exists(self.file_params["output_dir"]):
            os.rmdir(self.file_params["output_dir"])

        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):

            broken_sim = pe.routine.Simulation()
            broken_sim.configure(self.test_population, self.initial_sweeps,
                                 self.sweeps, self.sim_params,
                                 self.file_params)
            broken_sim.run_sweeps()
            patch_log.assert_called_once_with("NotImplementedError in"
                                              + " Simulation.run_sweeps()")
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.file_params["output_dir"]))

    @patch('os.makedirs')
    def test_write_to_file(self, mock_mkdir):

        if os.path.exists(self.file_params["output_dir"]):
            os.rmdir(self.file_params["output_dir"])

        mo = mock_open()
        self.file_params['age_stratified'] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            data = {s: 0 for s in list(pe.property.InfectionStatus)}
            data["age_group"] = len(pe.Parameters.instance().age_proportions)
            data["time"] = time

            with patch.object(test_sim.writer, 'write') as mock:
                test_sim.write_to_file(time)
                mock.assert_called_with(data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.file_params["output_dir"]))

        self.spatial_file_params['age_stratified'] = False
        self.file_params['age_stratified'] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params,
                               self.spatial_file_params)
            data = {s: 0 for s in list(pe.property.InfectionStatus)}
            data["time"] = time
            data["cell"] = test_sim.population.cells[0].id
            data['location_x'] = 0
            data['location_y'] = 0
            with patch.object(test_sim.writer, 'write') as mock:
                test_sim.write_to_file(time)
                mock.assert_called_with(data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.file_params["output_dir"]))
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
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.file_params["output_dir"]))

    @patch('os.makedirs')
    def test_s_write_to_file(self, mock_mkdir):
        # For spatial option to write to file
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            spatial_sim = pe.routine.Simulation()
            spatial_sim.configure(self.test_population, self.initial_sweeps,
                                  self.sweeps, self.sim_params,
                                  self.spatial_file_params)
            data = {s: 0 for s in list(pe.property.InfectionStatus)}
            data["age_group"] = len(pe.Parameters.instance().age_proportions)
            data["time"] = time
            cell = self.test_population.cells[0]
            data["cell"] = cell.id
            data["location_x"] = cell.location[0]
            data["location_y"] = cell.location[0]

            with patch.object(spatial_sim.writer, 'write') as mock:
                spatial_sim.write_to_file(time)
                mock.assert_called_with(data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.file_params["output_dir"]))

    @patch('os.makedirs')
    def test_write_to_ih_file(self, mock_mkdir):

        if os.path.exists(self.ih_file_params["output_dir"]):
            os.rmdir(self.ih_file_params["output_dir"])

        mo = mock_open()
        self.ih_file_params['status_output'] = True
        self.ih_file_params['infectiousness_output'] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.ih_file_params)
            data = {column: 0 for column in
                    test_sim.ih_status_writer.writer.fieldnames}
            data["time"] = time

        with patch.object(test_sim.ih_status_writer, 'write') as mock:
            test_sim.write_to_ih_file(time, "status")
            mock.assert_called_with(data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.ih_file_params["output_dir"]))

        self.ih_file_params['status_output'] = False
        self.ih_file_params['infectiousness_output'] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.ih_file_params)
            data = {column: 0 for column in
                    test_sim.ih_infectiousness_writer.writer.fieldnames}
            data["time"] = time

        with patch.object(test_sim.ih_infectiousness_writer, 'write') as mock:
            test_sim.write_to_ih_file(time, "infectiousness")
            mock.assert_called_with(data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.ih_file_params["output_dir"]))

        self.ih_file_params['status_output'] = True
        self.ih_file_params['infectiousness_output'] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.ih_file_params)
            ih_data = {column: 0 for column in
                       test_sim.ih_status_writer.writer.fieldnames}
            ih_data["time"] = time
            infect_data = {column: 0 for column in
                           test_sim.ih_infectiousness_writer.writer.fieldnames}
            infect_data["time"] = time

        with patch.object(test_sim.ih_status_writer, 'write') as mock:
            test_sim.write_to_ih_file(time, "status")
            mock.assert_called_with(ih_data)
        with patch.object(test_sim.ih_infectiousness_writer, 'write') as mock:
            test_sim.write_to_ih_file(time, "infectiousness")
            mock.assert_called_with(infect_data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.ih_file_params["output_dir"]))

    def test_set_random_seed(self):
        pe.routine.Simulation.set_random_seed(seed=0)
        value = random.random()
        np_value = np.random.random()
        self.assertAlmostEqual(value, 0.844422, places=5)
        self.assertAlmostEqual(np_value, 0.548814, places=5)
        # Values taken from known seed sequence

    @patch("numpy.random.seed")
    @patch("random.seed")
    @patch('os.makedirs')
    def test_random_seed_param(self, mock_mkdir, mock_random,
                               mock_np_random, n=42):
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            test_sim_params = self.sim_params.copy()
            test_sim_params["simulation_seed"] = n
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, test_sim_params, self.file_params)
        mock_random.assert_called_once_with(n)
        mock_np_random.assert_called_once_with(n)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.file_params["output_dir"]))

    @patch('os.makedirs')
    def test_add_writer(self, mock_mkdir):
        spatial_sim = pe.routine.Simulation()
        with patch('pyEpiabm.output._csv_writer.open'):
            spatial_sim.add_writer(pe.output.NewCasesWriter(
                os.path.join(os.getcwd(), self.file_params["output_dir"])))
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                      self.file_params["output_dir"]))


if __name__ == '__main__':
    unittest.main()
