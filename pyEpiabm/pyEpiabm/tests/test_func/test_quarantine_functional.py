import os
import pandas as pd
import unittest
from unittest.mock import patch, mock_open, Mock

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus


class TestQuarantineFunctional(unittest.TestCase):
    """Functional testing of household quarantine intervention. Conducts
    household quarantine intervention simulations with known
    results/properties to ensure code functions as desired.
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestQuarantineFunctional, cls).setUpClass()
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
                           "simulation_end_time": 12,
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
            "isolation_duration": 3,
            "isolation_probability": 1,
            "isolation_effectiveness": 1,
            "isolation_house_effectiveness": 1},

            "household_quarantine": {
            "start_time": 0,
            "policy_duration": 365,
            "case_threshold": 0,
            "quarantine_delay": 0,
            "quarantine_duration": 10,
            "quarantine_house_compliant": 1.0,
            "quarantine_individual_compliant": 1.0,
            "quarantine_house_effectiveness": 1.1,
            "quarantine_spatial_effectiveness": 0.1,
            "quarantine_place_effectiveness": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        }
        }

    @classmethod
    def tearDownClass(cls):
        super(TestQuarantineFunctional, cls).tearDownClass()
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
    def test_quarantine_present(self, mock_read, mock_csv):
        """Household quarantine functional test to ensure more people will be
        susceptible when household quarantine intervention is present.
        """
        mock_read.return_value = pd.DataFrame(self.pop_params)

        # Enable spatial infectious
        pe.routine.Simulation.set_random_seed(seed=30)
        pe.Parameters.instance().infection_radius = 1.6

        # Enable case isolation
        pe.Parameters.instance().intervention_params = {
            "case_isolation": self.intervention['case_isolation']}
        sweep_list = [
            pe.sweep.InterventionSweep(),
            pe.sweep.UpdatePlaceSweep(),
            pe.sweep.HouseholdSweep(),
            pe.sweep.PlaceSweep(),
            pe.sweep.SpatialSweep(),
            pe.sweep.QueueSweep(),
            pe.sweep.HostProgressionSweep(),
        ]
        pop_isolation = TestQuarantineFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params, sweep_list)

        # Enable both case isolation and household quarantine
        pe.Parameters.instance().intervention_params = self.intervention
        sweep_list = [
            pe.sweep.InterventionSweep(),
            pe.sweep.UpdatePlaceSweep(),
            pe.sweep.HouseholdSweep(),
            pe.sweep.PlaceSweep(),
            pe.sweep.SpatialSweep(),
            pe.sweep.QueueSweep(),
            pe.sweep.HostProgressionSweep(),
        ]
        pop_quarantine = TestQuarantineFunctional.file_simulation(
            "test_input.csv", self.sim_params, self.file_params, sweep_list)

        mock_read.assert_called_with('test_input.csv')
        self.assertEqual(mock_csv.call_count, 2)

        print('isolation')
        print(pop_isolation.cells[0].compartment_counter.retrieve()[
                        InfectionStatus.Susceptible])
        print(pop_quarantine.cells[0].compartment_counter.retrieve()[
                        InfectionStatus.Susceptible])

        # Compare number of susceptible individuals for each age group
        for age_group in range(len(pe.Parameters.instance().age_proportions)):
            with self.subTest(age_group=age_group):
                self.assertLessEqual(
                    pop_isolation.cells[0].compartment_counter.retrieve()[
                        InfectionStatus.Susceptible][age_group],
                    pop_quarantine.cells[0].compartment_counter.retrieve()[
                        InfectionStatus.Susceptible][age_group])
                self.assertLessEqual(
                    pop_isolation.cells[1].compartment_counter.retrieve()[
                        InfectionStatus.Susceptible][age_group],
                    pop_quarantine.cells[1].compartment_counter.retrieve()[
                        InfectionStatus.Susceptible][age_group])


if __name__ == '__main__':
    unittest.main()
