import os
import pandas as pd
import numpy as np
import unittest
from unittest.mock import patch, mock_open

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus
from pyEpiabm.tests import TestFunctional


@patch('pyEpiabm.routine.simulation.tqdm', TestFunctional.notqdm)
@patch('pyEpiabm.output._CsvDictWriter.write')
@patch('os.makedirs')
@patch("pandas.DataFrame.to_csv")
@patch("pandas.read_csv")
class TestSimFunctional(TestFunctional):
    """Functional testing of basic simulations. Conducts basic
    simulations with known results/properties to ensure code functions as
    desired.
    """

    def setUp(self) -> None:
        self.pop_params = {"population_size": 100, "cell_number": 1,
                           "microcell_number": 1, "household_number": 1,
                           "place_number": 2}
        self.sim_params = {"simulation_start_time": 0,
                           "simulation_end_time": 100,
                           "initial_infected_number": 0,
                           "include_waning": False}

        self.file_params = {"output_file": "output.csv",
                            "output_dir": "test_folder/integration_tests",
                            "spatial_output": False,
                            "age_stratified": True}

        self.read_params = {"filepath_or_buffer": 'test_input.csv',
                            "dtype": {"cell": int, "microcell": int}}

    @staticmethod
    def toy_simulation(pop_params, sim_params, file_params):
        # Create a population based on the parameters given.
        population = pe.routine.ToyPopulationFactory().make_pop(pop_params)

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
        del sim.writer
        del sim
        return population

    @staticmethod
    def file_simulation(pop_file, sim_params, file_params, sweep_list):
        # Create a population based on the parameters given.
        population = pe.routine.FilePopulationFactory.make_pop(pop_file)
        pe.routine.FilePopulationFactory.print_population(population,
                                                          "test.csv")

        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            sim = pe.routine.Simulation()
            sim.configure(
                population,
                [],
                sweep_list,
                sim_params,
                file_params)

            sim.run_sweeps()

        # Need to close the writer object at the end of each simulation.
        del sim.writer
        del sim
        return population

    def test_population_conservation(self, *mocks):
        """Basic functional test with a more complex population
        to ensure the simulation conserves basic population properties
        such as cell number.
        """
        pop_params = {"population_size": 500, "cell_number": 5,
                      "microcell_number": 2, "household_number": 5,
                      "place_number": 2}
        sim_params = {"simulation_start_time": 0, "simulation_end_time": 400,
                      "initial_infected_number": 10}
        iter_num = (sim_params["simulation_end_time"]
                    - sim_params["simulation_start_time"] + 1)

        pop = TestSimFunctional.toy_simulation(pop_params,
                                               sim_params,
                                               self.file_params)

        # Test size of simulation is as expected
        self.assertIsInstance(pop, pe.Population)
        self.assertEqual(len(pop.cells), pop_params["cell_number"])
        self.assertEqual(pop.total_people(), pop_params["population_size"])

        cell_count = len(pop.cells)
        mcell_count = 0
        place_count = 0
        for cell in pop.cells:
            mcell_count += len(cell.microcells)
            place_count += len(cell.places)

        self.assertEqual(mcell_count, (pop_params["microcell_number"]
                                       * pop_params["cell_number"]))
        self.assertEqual(place_count, (pop_params["place_number"]
                                       * pop_params["microcell_number"]
                                       * pop_params["cell_number"]))

        folder = os.path.join(os.getcwd(),
                              "test_folder/integration_tests")
        mocks[2].assert_called_with(folder)  # Mock for mkdir()
        nb_age_group = len(pe.Parameters.instance().age_proportions)
        mock_output_count = iter_num * nb_age_group * cell_count
        self.assertEqual(mocks[3].call_count, mock_output_count)

    def test_total_infection(self, *mocks):
        """Basic functional test to ensure everyone is infected when the entire
        population is placed in one large household.
        """
        self.sim_params["initial_infected_number"] = 5
        pop = TestSimFunctional.toy_simulation(self.pop_params,
                                               self.sim_params,
                                               self.file_params)

        # Test all individuals have recovered or died from infection at end
        final_state_count = 0
        for status in pe.property.InfectionStatus:
            with self.subTest(status=status):
                count = 0

                for cell in pop.cells:
                    cell_data = cell.compartment_counter.retrieve()
                    count += cell_data[status]
                if status in [InfectionStatus.Recovered, InfectionStatus.Dead]:
                    final_state_count += count
                else:
                    self.assertEqual(np.sum(count), 0)
        self.assertEqual(np.sum(final_state_count),
                         self.pop_params["population_size"])

        folder = os.path.join(os.getcwd(),
                              "test_folder/integration_tests")
        mocks[2].assert_called_with(folder)  # Mock for mkdir()

    def test_waning_compartments(self, *mocks):
        """Basic functional test to ensure everyone is not recovered at the
        end of the simulation.
        """
        self.sim_params["initial_infected_number"] = 5
        self.sim_params["include_waning"] = True
        pe.Parameters.instance().use_waning_immunity = 1.0

        pop = TestSimFunctional.toy_simulation(self.pop_params,
                                               self.sim_params,
                                               self.file_params)

        # Test not all individuals have entered Recovered or Dead at end
        recov_dead_state_count = 0

        for cell in pop.cells:
            cell_data = cell.compartment_counter.retrieve()
            for status in [InfectionStatus.Recovered,
                           InfectionStatus.Dead]:
                recov_dead_state_count += cell_data[status]

        self.assertNotEqual(np.sum(recov_dead_state_count),
                            self.pop_params["population_size"])

    def test_no_infection(self, *mocks):
        """Basic functional test to ensure noone is infected when there are
        no initial cases in the entire population
        """
        pop = TestSimFunctional.toy_simulation(self.pop_params,
                                               self.sim_params,
                                               self.file_params)

        # Test all individuals have remained Susceptible
        for status in pe.property.InfectionStatus:
            with self.subTest(status=status):
                count = 0

                for cell in pop.cells:
                    cell_data = cell.compartment_counter.retrieve()
                    count += cell_data[status]
                if status != InfectionStatus.Susceptible:
                    self.assertEqual(np.sum(count), 0)

    def test_segmented_infection(self, *mocks):
        """Basic functional test to ensure people cannot infect those
        outside their household (or microcell) without a spatial sweep.
        """
        mock_read, mock_csv = mocks[:2]
        file_input = {'cell': [1, 2], 'microcell': [1, 1],
                      'location_x': [0.0, 1.0], 'location_y': [0.0, 1.0],
                      'household_number': [1, 1],
                      'Susceptible': [8, 9], 'InfectMild': [2, 0]}
        mock_read.return_value = pd.DataFrame(file_input)

        sweep_list = [pe.sweep.HouseholdSweep(), pe.sweep.QueueSweep(),
                      pe.sweep.HostProgressionSweep()]

        pe.Parameters.instance().household_size_distribution = []
        pop = TestSimFunctional.file_simulation("test_input.csv",
                                                self.sim_params,
                                                self.file_params,
                                                sweep_list)

        mock_read.assert_called_with(**self.read_params)
        mock_csv.assert_called_once()

        cell_data_0 = pop.cells[0].compartment_counter.retrieve()
        cell_data_1 = pop.cells[1].compartment_counter.retrieve()
        self.assertEqual(np.sum(cell_data_0[InfectionStatus.Susceptible]), 0)
        self.assertEqual((np.sum(cell_data_0[InfectionStatus.Recovered])
                          + np.sum(cell_data_0[InfectionStatus.Dead])),
                         (file_input['Susceptible'][0]
                          + file_input["InfectMild"][0]))

        self.assertEqual(np.sum(cell_data_1[InfectionStatus.Susceptible]),
                         file_input['Susceptible'][1])
        self.assertEqual(np.sum(cell_data_1[InfectionStatus.Recovered]), 0)

    def test_small_cutoff(self, *mocks):
        """Basic functional test to ensure people cannot infect those
        outside their cell when the cut-off is sufficiently small.
        """
        mock_read, mock_csv = mocks[:2]
        file_input = {'cell': [1, 2], 'microcell': [1, 1],
                      'location_x': [0.0, 1.0], 'location_y': [0.0, 1.0],
                      'household_number': [1, 1],
                      'Susceptible': [8, 9], 'InfectMild': [2, 0]}
        mock_read.return_value = pd.DataFrame(file_input)

        sweep_list = [pe.sweep.HouseholdSweep(), pe.sweep.SpatialSweep(),
                      pe.sweep.QueueSweep(), pe.sweep.HostProgressionSweep()]

        pe.Parameters.instance().infection_radius = 0.5
        pop = TestSimFunctional.file_simulation("test_input.csv",
                                                self.sim_params,
                                                self.file_params,
                                                sweep_list)

        mock_read.assert_called_once_with(**self.read_params)
        mock_csv.assert_called_once()

        cell_data_0 = pop.cells[0].compartment_counter.retrieve()
        cell_data_1 = pop.cells[1].compartment_counter.retrieve()

        self.assertEqual(np.sum(cell_data_0[InfectionStatus.Susceptible]), 0)
        self.assertEqual((np.sum(cell_data_0[InfectionStatus.Recovered])
                          + np.sum(cell_data_0[InfectionStatus.Dead])),
                         (file_input['Susceptible'][0]
                          + file_input["InfectMild"][0]))

        self.assertEqual(np.sum(cell_data_1[InfectionStatus.Susceptible]),
                         file_input['Susceptible'][1])
        self.assertEqual(np.sum(cell_data_1[InfectionStatus.Recovered]), 0)

        # Now increase the cutoff to check the infection does spread
        pe.Parameters.instance().infection_radius = 1.5
        pop = TestSimFunctional.file_simulation("test_input.csv",
                                                self.sim_params,
                                                self.file_params,
                                                sweep_list)
        for i, cell in enumerate(pop.cells):
            with self.subTest(cell=cell):
                cell_data = pop.cells[i].compartment_counter.retrieve()
                self.assertEqual(0,
                                 np.sum(cell_data[InfectionStatus.Susceptible])
                                 )
                self.assertEqual((np.sum(cell_data[InfectionStatus.Recovered])
                                  + np.sum(cell_data[InfectionStatus.Dead])),
                                 (file_input['Susceptible'][i]
                                  + file_input["InfectMild"][i]))

    def test_waning_status_count(self, *mocks):
        """Basic functional test to ensure different number of people enter
        status categories given waning immunity.
        """
        # Record the number of individuals within the compartment Infect.Asympt
        # when waning immunity is active
        self.sim_params["initial_infected_number"] = 5
        self.sim_params["include_waning"] = True
        pe.Parameters.instance().use_waning_immunity = 1.0

        pop = TestSimFunctional.toy_simulation(self.pop_params,
                                               self.sim_params,
                                               self.file_params)

        count_with_waning = 0
        for cell in pop.cells:
            cell_data = cell.compartment_counter.retrieve()
            for status in [InfectionStatus.InfectASympt]:
                count_with_waning += cell_data[status]


        # Record the number of individuals within the compartment InfectAsympt
        # when waning immunity is not active
        pe.Parameters.instance().use_waning_immunity = 0.0
        self.sim_params["include_waning"] = False
        pop_2 = TestSimFunctional.toy_simulation(self.pop_params,
                                                 self.sim_params,
                                                 self.file_params)
        count_without_waning = 0

        for cell in pop_2.cells:
            cell_data = cell.compartment_counter.retrieve()
            for status in [InfectionStatus.InfectASympt]:
                count_without_waning += cell_data[status]

        # Compare the two values to ensure that when the rate multipliers
        # are applied, the number of individuals increases
        self.assertGreater(np.sum(count_with_waning),
                           np.sum(count_without_waning))


if __name__ == '__main__':
    unittest.main()
