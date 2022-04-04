import os
import unittest
from unittest.mock import patch, mock_open

import pyEpiabm as pe


class TestIntegrationWorkflows(unittest.TestCase):
    """Integration tests replicating example workflows
    with small population sizes (to minimise runtime).
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestIntegrationWorkflows, cls).setUpClass()

        filepath = os.path.join(os.path.dirname(__file__),
                                os.pardir, 'testing_parameters.json')
        pe.Parameters.set_file(filepath)

    @classmethod
    def tearDownClass(cls):
        if pe.Parameters._instance:
            pe.Parameters._instance = None

    def notqdm(iterable, *args, **kwargs):
        """Replacement for tqdm that just passes back the iterable
        useful to silence `tqdm` in tests
        """
        return iterable

    def basic_workflow_main():
        pop_params = {"population_size": 100, "cell_number": 1,
                      "microcell_number": 1, "household_number": 5,
                      "place_number": 2}

        # Create a population based on the parameters given.
        population = pe.routine.ToyPopulationFactory().make_pop(pop_params)

        sim_params = {"simulation_start_time": 0, "simulation_end_time": 60,
                      "initial_infected_number": 10}

        file_params = {"output_file": "output.csv",
                       "output_dir": "test_folder/integration_tests",
                       "spatial_output": False}

        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            sim = pe.routine.Simulation()
            sim.configure(
                population,
                [pe.sweep.InitialInfectedSweep()],
                [pe.sweep.HouseholdSweep(), pe.sweep.QueueSweep(),
                 pe.sweep.HostProgressionSweep()],
                sim_params,
                file_params)
            sim.run_sweeps()

        # Need to close the writer object at the end of each simulation.
        del(sim.writer)
        del(sim)
        return

    def spatial_workflow_main(generate_from_file: bool):
        pop_params = {
            "population_size": 500,
            "cell_number": 4,
            "microcell_number": 2,
            "household_number": 5,
        }

        if generate_from_file:
            file_loc = os.path.join(os.path.dirname(__file__),
                                    'spatial_input.csv')
            population = pe.routine.FilePopulationFactory.make_pop(file_loc)
        else:
            population = pe.routine.ToyPopulationFactory.make_pop(pop_params)
            pe.routine.ToyPopulationFactory.assign_cell_locations(population)
            pe.routine.FilePopulationFactory.print_population(population,
                                                              "output.csv")

        sim_params = {"simulation_start_time": 0, "simulation_end_time": 50,
                      "initial_infected_number": 1,
                      "initial_infect_cell": True}

        file_params = {"output_file": "output.csv",
                       "output_dir": "test_folder/integration_tests",
                       "spatial_output": True}

        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            sim = pe.routine.Simulation()
            sim.configure(
                population,
                [pe.sweep.InitialInfectedSweep()],
                [
                    pe.sweep.UpdatePlaceSweep(),
                    pe.sweep.HouseholdSweep(),
                    pe.sweep.SpatialSweep(),
                    pe.sweep.QueueSweep(),
                    pe.sweep.HostProgressionSweep(),
                ],
                sim_params,
                file_params,
            )
            sim.run_sweeps()

        # Need to close the writer object at the end of each simulation.
        del sim.writer
        del sim
        return

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write')
    @patch('os.makedirs')
    @patch('logging.warning')
    @patch('logging.error')
    def test_basic_workflow(self, mock_err, mock_warn,
                            mock_mkdir, mock_output):
        TestIntegrationWorkflows.basic_workflow_main()
        folder = os.path.join(os.getcwd(),
                              "test_folder/integration_tests")
        mock_mkdir.assert_called_with(folder)
        mock_err.assert_not_called()
        mock_warn.assert_not_called()

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write')
    @patch('pandas.DataFrame.to_csv')
    @patch('os.makedirs')
    @patch('logging.warning')
    @patch('logging.error')
    def test_spatial_workflow(self, mock_err, mock_warn,
                              mock_mkdir, mock_csv, mock_output):
        TestIntegrationWorkflows.spatial_workflow_main(False)
        folder = os.path.join(os.getcwd(),
                              "test_folder/integration_tests")
        mock_mkdir.assert_called_with(folder)
        self.assertEqual(mock_csv.call_args[0], ('output.csv',))
        mock_csv.assert_called_once()
        mock_err.assert_not_called()
        mock_warn.assert_not_called()

    @patch('pyEpiabm.routine.simulation.tqdm', notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write')
    @patch('os.makedirs')
    @patch('logging.warning')
    @patch('logging.error')
    def test_spatial_workflow_file_pop(self, mock_err, mock_warn,
                                       mock_mkdir, mock_output):
        TestIntegrationWorkflows.spatial_workflow_main(True)
        folder = os.path.join(os.getcwd(),
                              "test_folder/integration_tests")
        mock_mkdir.assert_called_with(folder)
        mock_err.assert_not_called()
        mock_warn.assert_not_called()


if __name__ == '__main__':
    unittest.main()
