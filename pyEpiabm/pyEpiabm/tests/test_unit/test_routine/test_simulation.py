import os
import sys
import random
import numpy as np
import unittest
from unittest.mock import patch, mock_open, MagicMock, call

import pyEpiabm as pe

from pyEpiabm.tests.test_unit.mocked_logging_tests import TestMockedLogs


class TestSimulation(TestMockedLogs):
    """Tests the 'Simulation' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super(TestSimulation, cls).setUpClass()  # Sets up patch on logging
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 1, "cell_number": 1,
                          "microcell_number": 1, "household_number": 1}
        cls.test_population = cls.pop_factory.make_pop(cls.pop_params)
        cls.rt_pop_params = {"population_size": 3, "cell_number": 1,
                             "microcell_number": 1, "household_number": 1}
        cls.rt_test_population = cls.pop_factory.make_pop(cls.rt_pop_params)
        pe.Parameters.instance().time_steps_per_day = 1
        cls.sim_params = {"simulation_start_time": 0,
                          "simulation_end_time": 1,
                          "initial_infected_number": 0,
                          "include_waning": True}

        cls.mock_output_dir = "pyEpiabm/pyEpiabm/tests/test_output/mock"
        cls.file_params = {"output_file": "test_file.csv",
                           "output_dir": cls.mock_output_dir}
        cls.inf_history_params = {"output_dir": cls.mock_output_dir,
                                  "status_output": False,
                                  "infectiousness_output": False,
                                  "secondary_infections_output": False}
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

            # Test configure binds parameters as expected, with default
            # input for inf_history_params
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            self.assertEqual(len(test_sim.initial_sweeps), 1)
            self.assertEqual(len(test_sim.sweeps), 1)
            self.assertIsInstance(test_sim.population, pe.Population)

            # Test that the ih writers are None, that status_output,
            # infectiousness_output and secondary_infections_output are False,
            # and that compress is false
            self.assertEqual(test_sim.status_output, False)
            self.assertEqual(test_sim.infectiousness_output, False)
            self.assertEqual(test_sim.secondary_infections_output, False)
            self.assertEqual(test_sim.ih_status_writer, None)
            self.assertEqual(test_sim.ih_infectiousness_writer, None)
            self.assertEqual(test_sim.secondary_infections_writer, None)
            self.assertEqual(test_sim.include_waning, True)
            self.assertEqual(test_sim.compress, False)

            del test_sim.writer
            del test_sim.ih_status_writer
            del test_sim.ih_infectiousness_writer
            del test_sim.secondary_infections_writer
        mo.assert_called_with(filename, 'w')

    @patch('os.makedirs')
    @patch('logging.warning')
    def test_configure_ih_status_infectiousness_false(self, mock_warning,
                                                      mock_dir):
        self.inf_history_params["infectiousness_output"] = False
        self.inf_history_params["status_output"] = False
        self.inf_history_params["secondary_infections_output"] = False
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            mock_warning.assert_called_once_with("status_output, "
                                                 "infectiousness_output and "
                                                 "secondary_infections_output "
                                                 "are False. No infection "
                                                 "history csvs will be "
                                                 "created.")

    @patch('os.makedirs')
    def test_configure_ih_status(self, mock_mkdir):
        mo = mock_open()
        self.inf_history_params["infectiousness_output"] = False
        self.inf_history_params["status_output"] = True
        self.inf_history_params["secondary_infections_output"] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            filename = os.path.join(os.getcwd(),
                                    self.inf_history_params["output_dir"],
                                    "inf_status_history.csv")
            test_sim = pe.routine.Simulation()

            # Test that the output titles are correct
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)

            self.assertEqual(test_sim.ih_output_titles, ["time", '0.0.0.0'])
            # Test that the ih_infectiousness_writer is None, as
            # infectiousness_output is False
            self.assertEqual(test_sim.ih_infectiousness_writer, None)
            self.assertEqual(test_sim.secondary_infections_writer, None)

            del test_sim.writer
            del test_sim.ih_status_writer
            del test_sim.ih_infectiousness_writer
            del test_sim.secondary_infections_writer
        mo.assert_called_with(filename, 'w')

    @patch('os.makedirs')
    def test_configure_ih_infectiousness(self, mock_mkdir):
        mo = mock_open()
        self.inf_history_params["infectiousness_output"] = True
        self.inf_history_params["status_output"] = False
        self.inf_history_params["secondary_infections_output"] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            filename = os.path.join(os.getcwd(),
                                    self.inf_history_params["output_dir"],
                                    "infectiousness_history.csv")
            test_sim = pe.routine.Simulation()

            # Test that the output titles are correct
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)

            self.assertEqual(test_sim.ih_output_titles, ["time", '0.0.0.0'])
            # Test that the ih_status_writer is None, as
            # infectiousness_output is False
            self.assertEqual(test_sim.ih_status_writer, None)
            self.assertEqual(test_sim.secondary_infections_writer, None)

            del test_sim.writer
            del test_sim.ih_status_writer
            del test_sim.ih_infectiousness_writer
            del test_sim.secondary_infections_writer
        mo.assert_called_with(filename, 'w')

    @patch('os.makedirs')
    def test_configure_secondary_infections(self, mock_mkdir):
        mo = mock_open()
        self.inf_history_params["infectiousness_output"] = False
        self.inf_history_params["status_output"] = False
        self.inf_history_params["secondary_infections_output"] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            filename = os.path.join(os.getcwd(),
                                    self.inf_history_params["output_dir"],
                                    "secondary_infections.csv")
            test_sim = pe.routine.Simulation()

            # Test that the output titles are correct
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)

            self.assertEqual(test_sim.Rt_output_titles,
                             ["time", '0.0.0.0', "R_t"])
            # Test that the ih_status_writer is None, as
            # infectiousness_output is False
            self.assertEqual(test_sim.ih_status_writer, None)
            self.assertEqual(test_sim.ih_infectiousness_writer, None)

            del test_sim.writer
            del test_sim.ih_status_writer
            del test_sim.ih_infectiousness_writer
            del test_sim.secondary_infections_writer
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
                                                       self.file_params[
                                                           "output_dir"]))

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
    @patch('pyEpiabm.routine.Simulation.write_to_ih_file')
    @patch('os.makedirs')
    def test_run_sweeps_ih_status(self, mock_mkdir, patch_write):
        mo = mock_open()
        self.inf_history_params["infectiousness_output"] = False
        self.inf_history_params["status_output"] = True
        self.inf_history_params["secondary_infections_output"] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time_write = self.sim_params["simulation_end_time"]
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            test_sim.run_sweeps()
            patch_write.assert_called_with(time_write, output_option="status")

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.routine.Simulation.write_to_ih_file')
    @patch('os.makedirs')
    def test_run_sweeps_ih_infectiousness(self, mock_mkdir, patch_write):
        mo = mock_open()
        self.inf_history_params["infectiousness_output"] = True
        self.inf_history_params["status_output"] = False
        self.inf_history_params["secondary_infections_output"] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time_write = self.sim_params["simulation_end_time"]
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            test_sim.run_sweeps()
            patch_write.assert_called_with(time_write,
                                           output_option="infectiousness")

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.routine.Simulation.write_to_Rt_file')
    @patch('os.makedirs')
    def test_run_sweeps_secondary_infections(self, mock_mkdir, patch_write):
        mo = mock_open()
        self.inf_history_params["infectiousness_output"] = False
        self.inf_history_params["status_output"] = False
        self.inf_history_params["secondary_infections_output"] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            test_sim.run_sweeps()
            patch_write.assert_called_with(np.array([1]))

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
                                                   self.file_params[
                                                       "output_dir"]))

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
                                                   self.file_params[
                                                       "output_dir"]))

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
            for cell in self.test_population.cells:
                for age_i in \
                        range(0,
                              len(pe.Parameters.instance().age_proportions)):
                    for inf_status in list(pe.property.InfectionStatus):
                        data_per_inf_status = \
                                cell.compartment_counter.retrieve()[inf_status]
                        data[inf_status] += data_per_inf_status[age_i]
            data["age_group"] = len(pe.Parameters.instance().age_proportions)
            data["time"] = time

            with patch.object(test_sim.writer, 'write') as mock:
                test_sim.write_to_file(time)
                mock.assert_called_with(data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.file_params[
                                                       "output_dir"]))

        self.spatial_file_params['age_stratified'] = False
        self.file_params['age_stratified'] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params,
                               self.spatial_file_params)
            data = {s: 0 for s in list(pe.property.InfectionStatus)}
            for cell in self.test_population.cells:
                for k in data:
                    data[k] += sum(cell.compartment_counter.retrieve()[k])
                data["time"] = time
                data["cell"] = test_sim.population.cells[0].id
                data['location_x'] = 0
                data['location_y'] = 0
            with patch.object(test_sim.writer, 'write') as mock:
                test_sim.write_to_file(time)
                mock.assert_called_with(data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.file_params[
                                                       "output_dir"]))

        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            data = {s: 0 for s in list(pe.property.InfectionStatus)}
            for cell in self.test_population.cells:
                for k in data:
                    data[k] += sum(cell.compartment_counter.retrieve()[k])
            data["time"] = time
            with patch.object(test_sim.writer, 'write') as mock:
                test_sim.write_to_file(time)
                mock.assert_called_with(data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.file_params[
                                                       "output_dir"]))

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
            for cell in self.test_population.cells:
                for age_i in \
                        range(0,
                              len(pe.Parameters.instance().age_proportions)):
                    data = {s: 0 for s in list(pe.property.InfectionStatus)}
                    for inf_status in data:
                        data_per_inf_status = \
                                cell.compartment_counter.retrieve()[inf_status]
                        data[inf_status] += data_per_inf_status[age_i]
                data["age_group"] = \
                    len(pe.Parameters.instance().age_proportions)
                data["time"] = time
                cell = self.test_population.cells[0]
                data["cell"] = cell.id
                data["location_x"] = cell.location[0]
                data["location_y"] = cell.location[0]

            with patch.object(spatial_sim.writer, 'write') as mock:
                spatial_sim.write_to_file(time)
                mock.assert_called_with(data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.file_params[
                                                       "output_dir"]))

    @patch('os.makedirs')
    def test_write_to_ih_file_status_no_infectiousness(self, mock_mkdir,
                                                       time=1):

        if os.path.exists(self.inf_history_params["output_dir"]):
            os.rmdir(self.inf_history_params["output_dir"])

        mo = mock_open()
        self.inf_history_params['status_output'] = True
        self.inf_history_params['infectiousness_output'] = False
        self.inf_history_params['secondary_infections_output'] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            data = {column: 0 for column in
                    test_sim.ih_status_writer.writer.fieldnames}
            for cell in self.test_population.cells:
                for person in cell.persons:
                    data[person.id] = person.infection_status.value
            data["time"] = time

            with patch.object(test_sim.ih_status_writer, 'write') as mock:
                test_sim.write_to_ih_file(time, "status")
                mock.assert_called_with(data)
        mock_mkdir.assert_called_with(
            os.path.join(os.getcwd(), self.inf_history_params["output_dir"]))

    @patch('os.makedirs')
    def test_write_to_ih_file_no_status_infectiousness(self, mock_mkdir,
                                                       time=1):

        if os.path.exists(self.inf_history_params["output_dir"]):
            os.rmdir(self.inf_history_params["output_dir"])

        mo = mock_open()
        self.inf_history_params['status_output'] = False
        self.inf_history_params['infectiousness_output'] = True
        self.inf_history_params['secondary_infections_output'] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            data = {column: 0 for column in
                    test_sim.ih_infectiousness_writer.writer.fieldnames}
            for cell in self.test_population.cells:
                for person in cell.persons:
                    data[person.id] = person.infectiousness
            data["time"] = time

            with patch.object(test_sim.ih_infectiousness_writer, 'write') \
                    as mock:
                test_sim.write_to_ih_file(time, "infectiousness")
                mock.assert_called_with(data)
        mock_mkdir.assert_called_with(
            os.path.join(os.getcwd(), self.inf_history_params["output_dir"]))

    @patch('os.makedirs')
    def test_write_to_ih_file_status_infectiousness(self, mock_mkdir, time=1):

        if os.path.exists(self.inf_history_params["output_dir"]):
            os.rmdir(self.inf_history_params["output_dir"])

        mo = mock_open()
        self.inf_history_params['status_output'] = True
        self.inf_history_params['infectiousness_output'] = True
        self.inf_history_params['secondary_infections_output'] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            ih_data = {column: 0 for column in
                       test_sim.ih_status_writer.fieldnames}
            for cell in self.test_population.cells:
                for person in cell.persons:
                    ih_data[person.id] = person.infection_status.value
            ih_data["time"] = time
            infect_data = {column: 0 for column in
                           test_sim.ih_infectiousness_writer.fieldnames}
            for cell in self.test_population.cells:
                for person in cell.persons:
                    infect_data[person.id] = person.infectiousness
            infect_data["time"] = time

            with patch.object(test_sim.ih_status_writer, 'write') as mock:
                test_sim.write_to_ih_file(time, "status")
                mock.assert_called_with(ih_data)
            with patch.object(test_sim.ih_infectiousness_writer, 'write') \
                    as mock:
                test_sim.write_to_ih_file(time, "infectiousness")
                mock.assert_called_with(infect_data)
        mock_mkdir.assert_called_with(
            os.path.join(os.getcwd(), self.inf_history_params["output_dir"]))

    @patch('os.makedirs')
    def test_write_to_Rt_file(self, mock_mkdir, time=1):

        if os.path.exists(self.inf_history_params["output_dir"]):
            os.rmdir(self.inf_history_params["output_dir"])

        mo = mock_open()
        self.inf_history_params['status_output'] = False
        self.inf_history_params['infectiousness_output'] = False
        self.inf_history_params['secondary_infections_output'] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.rt_test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            person1 = self.rt_test_population.cells[0].persons[0]
            person1.num_times_infected = 1
            person1.infection_start_times = [1.0]
            person1.secondary_infections_counts = [5]
            person2 = self.rt_test_population.cells[0].persons[1]
            person2.num_times_infected = 1
            person2.infection_start_times = [0.0]
            person2.secondary_infections_counts = [7]
            person3 = self.rt_test_population.cells[0].persons[2]
            person3.num_times_infected = 1
            person3.infection_start_times = [1.0]
            person3.secondary_infections_counts = [8]
            dict_1 = {"time": 0, "0.0.0.0": np.nan, "0.0.0.1": 7.0,
                      "0.0.0.2": np.nan, "R_t": 7.0}
            dict_2 = {"time": 1, "0.0.0.0": 5.0, "0.0.0.1": np.nan,
                      "0.0.0.2": 8.0, "R_t": 6.5}
            dict_3 = {"time": 2, "0.0.0.0": np.nan, "0.0.0.1": np.nan,
                      "0.0.0.2": np.nan, "R_t": np.nan}

            with patch('pyEpiabm.output._csv_dict_writer'
                       '._CsvDictWriter.write') as mock_write:
                test_sim.write_to_Rt_file(np.array([1, 2]))
                calls = mock_write.call_args_list
                # Need to use np.testing for the NaNs
                # Need to test keys and values separately in case we are using
                # python 3.7 (for which np.testing.assert_equal will not work)
                if sys.version_info[0] >= 3 or sys.version_info[1] >= 8:
                    actual_dict_1 = calls[0].args[0]
                    for key in dict_1:
                        self.assertTrue(key in actual_dict_1)
                        np.testing.assert_array_equal(dict_1[key],
                                                      actual_dict_1[key])
                    actual_dict_2 = calls[1].args[0]
                    for key in dict_2:
                        self.assertTrue(key in actual_dict_2)
                        np.testing.assert_array_equal(dict_2[key],
                                                      actual_dict_2[key])
                    actual_dict_3 = calls[2].args[0]
                    for key in dict_3:
                        self.assertTrue(key in actual_dict_3)
                        np.testing.assert_array_equal(dict_3[key],
                                                      actual_dict_3[key])
                    self.assertEqual(mock_write.call_count, 3)
        mock_mkdir.assert_called_with(
            os.path.join(os.getcwd(), self.inf_history_params["output_dir"]))

    @patch('os.makedirs')
    def test_compress_no_compression(self, mock_mkdir):
        mo = mock_open()
        self.inf_history_params['compress'] = False
        self.inf_history_params['status_output'] = True
        self.inf_history_params['infectiousness_output'] = True
        self.inf_history_params['secondary_infections_output'] = True

        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            mock_status_writer = MagicMock()
            mock_infectiousness_writer = MagicMock()
            mock_rt_writer = MagicMock()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            test_sim.run_sweeps()

            with patch.object(test_sim, 'ih_status_writer',
                              mock_status_writer):
                with patch.object(test_sim, 'ih_infectiousness_writer',
                                  mock_infectiousness_writer):
                    with patch.object(test_sim, 'secondary_infections_writer',
                                      mock_rt_writer):
                        test_sim.compress_csv()
                        mock_status_writer.compress.assert_not_called()
                        mock_infectiousness_writer.compress.assert_not_called()
                        mock_rt_writer.assert_not_called()
            del test_sim

    @patch('os.makedirs')
    def test_compress_csv_status(self, mock_mkdir):
        mo = mock_open()
        self.inf_history_params['compress'] = True
        self.inf_history_params['status_output'] = True
        self.inf_history_params['infectiousness_output'] = False
        self.inf_history_params['secondary_infections_output'] = False

        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            mock_status_writer = MagicMock()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            test_sim.run_sweeps()
            with patch.object(test_sim, 'ih_status_writer',
                              mock_status_writer):
                test_sim.compress_csv()
                mock_status_writer.compress.assert_called_once_with()
            del test_sim

    @patch('os.makedirs')
    def test_compress_csv_infect(self, mock_mkdir):
        mo = mock_open()
        self.inf_history_params['compress'] = True
        self.inf_history_params['status_output'] = False
        self.inf_history_params['infectiousness_output'] = True
        self.inf_history_params['secondary_infections_output'] = False

        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            mock_infect_writer = MagicMock()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            test_sim.run_sweeps()
            with patch.object(test_sim, 'ih_infectiousness_writer',
                              mock_infect_writer):
                test_sim.compress_csv()
                mock_infect_writer.compress.assert_called_once_with()
            del test_sim

    @patch('os.makedirs')
    def test_compress_csv_secondary_infections(self, mock_mkdir):
        mo = mock_open()
        self.inf_history_params['compress'] = True
        self.inf_history_params['status_output'] = False
        self.inf_history_params['infectiousness_output'] = False
        self.inf_history_params['secondary_infections_output'] = True

        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            test_sim = pe.routine.Simulation()
            mock_rt_writer = MagicMock()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params,
                               self.inf_history_params)
            test_sim.run_sweeps()
            with patch.object(test_sim, 'secondary_infections_writer',
                              mock_rt_writer):
                test_sim.compress_csv()
                mock_rt_writer.compress.assert_called_once_with()
            del test_sim

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
                                                   self.file_params[
                                                       "output_dir"]))

    @patch('os.makedirs')
    def test_add_writer(self, mock_mkdir):
        spatial_sim = pe.routine.Simulation()
        with patch('pyEpiabm.output._csv_writer.open'):
            spatial_sim.add_writer(pe.output.NewCasesWriter(
                os.path.join(os.getcwd(), self.file_params["output_dir"])))
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.file_params[
                                                       "output_dir"]))


if __name__ == '__main__':
    unittest.main()
