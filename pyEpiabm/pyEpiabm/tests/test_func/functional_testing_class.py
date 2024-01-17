#
# Custom testing class to patch logging
#

from unittest.mock import patch, mock_open

import pyEpiabm as pe
from pyEpiabm.tests.test_unit import TestMockedLogs


class TestFunctional(TestMockedLogs):
    """Inherits from the custom testing class, which is
    the unittest.TestCase class with a parameters file bolted
    on and mocked logging functions to prevent printing.

    Contains class methods to silence tqdm progress bars and
    set up populations for ease of use when running repeated
    simulations to evaluate intervention effectiveness.

    """
    @staticmethod
    def notqdm(iterable, *args, **kwargs):
        """Replacement for tqdm that just passes back the iterable
        useful to silence `tqdm` in tests.
        """
        return iterable

    @classmethod
    def setUpPopulation(self):
        """Can be called in setUp to create a default population,
        to test the impact of interventions.
        """
        self.pop_params = {'cell': [1, 2], 'microcell': [1, 1],
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

    @classmethod
    def file_simulation(self, pop_file, sim_params, file_params, sweep_list):
        """ Creates a population based on the parameter dicts given.

        Parameters
        ----------
        pop_file : dstr
            Path to input file which stores population
        sim_params : dict
            Dictionary of parameters specific to the simulation used and used
            as input for call method of initial sweeps
        file_params : dict
            Dictionary of parameters specific to the output file
        sweep_list : typing.List
            List of sweeps used in the simulation

        """
        population = pe.routine.FilePopulationFactory.make_pop(
            pop_file, random_seed=30)
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
