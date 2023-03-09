import os
import random
import pandas as pd
from parameterized import parameterized
import unittest
from unittest.mock import patch, mock_open

import pyEpiabm as pe
from pyEpiabm.tests import TestFunctional
from pyEpiabm.tests.test_func import HelperFunc

numReps = 2


class TestPopulationRandomSeeds(TestFunctional):
    """Test random seed usage in population generation
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestPopulationRandomSeeds, cls).setUpClass()
        pe.Parameters.instance().household_size_distribution = []

    def setUp(self) -> None:
        self.input = {'cell': [1.0, 2.0], 'microcell': [1.0, 1.0],
                      'location_x': [0.0, 1.0], 'location_y': [0.0, 1.0],
                      'household_number': [1, 1],
                      'Susceptible': [8, 9], 'InfectMild': [2, 3]}
        self.df = pd.DataFrame(self.input)

    def summarise_households(self, pop: pe.Population):
        # Returns lists of cell and microcell wise populations
        # Not a testing function, but used in test below

        households = []
        sizes = []
        for cell in pop.cells:
            for microcell in cell.microcells:
                for person in microcell.persons:
                    if person.household not in households:
                        households.append(person.household)
                        sizes.append(len(person.household.persons))
        return sizes

    @patch("pandas.read_csv")
    def test_household_seed(self, mock_read):
        """Tests household allocation is consistent with random seed
        """
        input = {'cell': [1, 2], 'microcell': [1, 1],
                 'household_number': [10, 10],
                 'Susceptible': [200, 200]}
        df = pd.DataFrame(input)
        mock_read.return_value = df

        # Create two identical populations with the same seed
        seed_pop = pe.routine.FilePopulationFactory.make_pop('mock_file', 42)
        comp_pop = pe.routine.FilePopulationFactory.make_pop('mock_file', 42)

        self.assertEqual(str(seed_pop), str(comp_pop))

        seed_households = self.summarise_households(seed_pop)
        comp_households = self.summarise_households(comp_pop)
        self.assertEqual(seed_households, comp_households)

        # Also compare to a population with a different seed
        diff_pop = pe.routine.FilePopulationFactory().make_pop('mock_file', 43)

        diff_households = self.summarise_households(diff_pop)
        self.assertNotEqual(seed_households, diff_households)

    def summarise_pop(self, pop):
        # Returns lists of cell and microcell wise populations
        # Not a testing function, but used in test below

        pop_cells = []  # List of populations in each cell of population
        pop_microcells = []  # List of populations in each microcell
        for cell in pop.cells:
            pop_cells.append(len(cell.persons))
            for microcell in cell.microcells:
                pop_microcells.append(len(microcell.persons))
        return pop_cells, pop_microcells

    @parameterized.expand([(random.randint(1000, 10000),
                            random.randint(5, 10),
                            random.randint(2, 10),
                            random.randint(1, 100))
                          for _ in range(numReps)])
    def test_pop_seed(self, pop_size, cell_number, microcell_number, seed):
        """Tests for when the population is implemented by default with
        no households. Parameters are assigned at random.
        """
        # Define parameters for population generation
        pop_params = {"population_size": pop_size, "cell_number": cell_number,
                      "microcell_number": microcell_number,
                      "population_seed": seed}

        # Create two identical populations with the same seed
        seed_pop = pe.routine.ToyPopulationFactory.make_pop(pop_params)
        comp_pop = pe.routine.ToyPopulationFactory.make_pop(pop_params)

        self.assertEqual(str(seed_pop), str(comp_pop))

        seed_cells, seed_microcells = self.summarise_pop(seed_pop)
        comp_cells, comp_microcells = self.summarise_pop(comp_pop)
        self.assertEqual(seed_cells, comp_cells)
        self.assertEqual(seed_microcells, comp_microcells)

        # Also compare to a population with a different seed
        pop_params["population_seed"] = seed + 1  # Change seed of population
        diff_pop = pe.routine.ToyPopulationFactory().make_pop(pop_params)

        diff_cells, diff_microcells = self.summarise_pop(diff_pop)
        self.assertNotEqual(seed_cells, diff_cells)
        self.assertNotEqual(seed_microcells, diff_microcells)


class TestSimulationRandomSeeds(TestFunctional):
    """Test random seed usage in simulation evaluation
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestSimulationRandomSeeds, cls).setUpClass()
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
                           "output_dir": cls.mock_output_dir,
                           "age_stratified": True}

        cls.spatial_file_params = dict(cls.file_params)
        cls.spatial_file_params["spatial_output"] = True

        cls.initial_sweeps = [pe.sweep.InitialInfectedSweep()]
        cls.sweeps = [pe.sweep.PlaceSweep()]


    @patch('pyEpiabm.routine.simulation.tqdm', TestFunctional.notqdm)
    @patch('pyEpiabm.output._CsvDictWriter.write')
    @patch('os.makedirs')
    def test_random_seed(self, mock_mkdir, mock_write):
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

        folder = os.path.join(os.getcwd(), self.mock_output_dir)
        mock_mkdir.assert_called_with(folder)
        self.assertEqual(mock_mkdir.call_count, 3)
        self.assertEqual(seed_output, comp_output)
        self.assertNotEqual(seed_output, diff_output)


if __name__ == '__main__':
    unittest.main()
