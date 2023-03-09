#
# Custom testing class to patching logging
#

from unittest.mock import patch, mock_open

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestFunctional(TestPyEpiabm):
    """Inherits from the custom testing function, which is
    the unittest.TestCase class with a parameters file bolted
    on, but with mocked logging functions to prevent printing

    """
    @classmethod
    def setUpClass(cls):
        """Inherits from the unittest setup, and patches the warning
        and error logging classes, that otherwise print to terminal.
        """
        super(TestFunctional, cls).setUpClass()
        cls.warning_patcher = patch('logging.warning')
        cls.error_patcher = patch('logging.error')

        cls.warning_patcher.start()
        cls.error_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Inherits from the unittest teardown, and remove all patches.
        """
        super(TestFunctional, cls).tearDownClass()
        cls.warning_patcher.stop()
        cls.error_patcher.stop()

    @staticmethod
    def notqdm(iterable, *args, **kwargs):
        """Replacement for tqdm that just passes back the iterable
        useful to silence `tqdm` in tests.
        """
        return iterable

    @classmethod
    def setUpPopulation(self):
        """Can be called in setUp to create a default population.
        """
        self.pop_params = {'cell': [1.0, 2.0], 'microcell': [1.0, 1.0],
                           'location_x': [0.0, 1.0], 'location_y': [0.0, 1.0],
                           'household_number': [1, 1],
                           'Susceptible': [80, 90], 'InfectMild': [10, 0],
                           'place_number': 6}
        self.sim_params = {"simulation_start_time": 0,
                           "simulation_end_time": 15,
                           "initial_infected_number": 0}

        self.file_params = {"output_file": "output.csv",
                            "output_dir": "test_folder/integration_tests",
                            "spatial_output": False,
                            "age_stratified": True}

    @classmethod
    def file_simulation(self, pop_file, sim_params, file_params, sweep_list):
        # Create a population based on the parameters given.
        population = pe.routine.FilePopulationFactory.make_pop(
            pop_file, random_seed=40)
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
