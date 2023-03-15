import os
import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm
from pyEpiabm.core import Parameters


class TestInitialInfectedSweep(TestPyEpiabm):
    """Test the 'InitialInfectedSweep' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up a population we can use throughout the test.
        2 people are located in one microcell.
        """
        super(TestInitialInfectedSweep, cls).setUpClass()
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 2, "cell_number": 1,
                          "microcell_number": 1, "household_number": 1}
        cls.test_population = cls.pop_factory.make_pop(cls.pop_params)
        cls.cell = cls.test_population.cells[0]
        cls.microcell = cls.cell.microcells[0]
        cls.person1 = cls.cell.microcells[0].persons[0]
        cls.person2 = cls.test_population.cells[0].microcells[0].persons[1]

    def setUp(self) -> None:
        """This reinitialises the parameters singleton before every test
        (default behaviour is only once per class). This allows modification
        of the parameters in each test without side effects to others.
        """
        filepath = os.path.join(os.path.dirname(__file__), os.pardir,
                                os.pardir, 'testing_parameters.json')
        pe.Parameters.set_file(filepath)

    def test_call(self):
        """Test the main function of the Initial Infected Sweep.
        """
        test_sweep = pe.sweep.InitialInfectedSweep()
        test_sweep.bind_population(self.test_population)
        # Test asking for more infected people than the population number
        # raises an error.
        params = {"initial_infected_number": 4, "simulation_start_time": 0}
        self.assertRaises(ValueError, test_sweep, params)

        # Test asking negative start time
        params = {"initial_infected_number": 1, "simulation_start_time": -2}
        self.assertRaises(ValueError, test_sweep, params)

        # Test that summed initial infectiousness from individuals is zero
        # before call
        summed_inf = 0
        for person in self.microcell.persons:
            summed_inf += person.initial_infectiousness
        self.assertEqual(summed_inf, 0)

        # Test that call assigns correct number of infectious people.
        params = {"initial_infected_number": 1, "simulation_start_time": 0}
        test_sweep(params)
        status = pe.property.InfectionStatus.InfectMild
        num_infectious = sum(self.cell.compartment_counter.retrieve()[status])
        self.assertEqual(num_infectious, 1)

        # Test functions when initial infected cell given.
        params = {"initial_infected_number": 1, "simulation_start_time": 0,
                  "initial_infect_cell": 1}
        self.person1.update_status(pe.property.InfectionStatus.Susceptible)
        self.person2.update_status(pe.property.InfectionStatus.Susceptible)
        test_sweep(params)
        status = pe.property.InfectionStatus.InfectMild
        num_infectious = sum(self.cell.compartment_counter.retrieve()[status])
        self.assertEqual(num_infectious, 1)

        # Test that summed initial infectiousness from individuals is non-zero
        for person in self.microcell.persons:
            summed_inf += person.initial_infectiousness
        self.assertGreater(summed_inf, 0)

        # Test that trying to infect a population without enough
        # susceptible people raises an error.
        self.person1.update_status(pe.property.InfectionStatus.Recovered)
        self.person2.update_status(pe.property.InfectionStatus.Recovered)
        params = {"initial_infected_number": 1, "simulation_start_time": 0}
        self.assertRaises(ValueError, test_sweep, params)

    def test_carehome_options(self):
        """ Test that call assigns correct number of infectious people when \
        have carehome initial infections.
        """
        test_sweep = pe.sweep.InitialInfectedSweep()
        test_sweep.bind_population(self.test_population)

        # Set parameters and initial susceptibility
        params = {"initial_infected_number": 1, "simulation_start_time": 0}
        self.person1.update_status(pe.property.InfectionStatus.Susceptible)
        self.person2.update_status(pe.property.InfectionStatus.Susceptible)
        self.person1.age = 80
        self.person1.care_home_resident = True

        test_sweep(params)
        status = pe.property.InfectionStatus.InfectMild
        num_infectious = sum(self.cell.compartment_counter.retrieve()[status])
        self.assertEqual(num_infectious, 1)
        self.assertEqual(self.person2.infection_status, status)

        # Set parameters and initial susceptibilty to test error
        params = {"initial_infected_number": 2, "simulation_start_time": 0}
        self.person1.update_status(pe.property.InfectionStatus.Susceptible)
        self.person2.update_status(pe.property.InfectionStatus.Susceptible)
        self.person1.age = 80
        self.person1.care_home_resident = True

        self.assertRaises(ValueError, test_sweep, params)

        # Test functions if no carehome parameters given
        delattr(Parameters.instance(), 'carehome_params')
        test_sweep(params)
        status = pe.property.InfectionStatus.InfectMild
        num_infectious = sum(self.cell.compartment_counter.retrieve()[status])
        self.assertEqual(num_infectious, 2)

    @mock.patch('logging.warning')
    def test_logging(self, mock_log):
        """Test the Initial Infected Sweep for logging messages.
        """
        test_sweep = pe.sweep.InitialInfectedSweep()
        test_sweep.bind_population(self.test_population)
        # Test asking for non-integer infected people
        # raises a logging warning.
        params = {"initial_infected_number": 0.2, "simulation_start_time": 0}
        test_sweep(params)
        mock_log.assert_called_once_with("Initial number of infected people "
                                         + "needs to be an integer so we use "
                                         + "floor function to round down. "
                                         + "Inputed value was 0.2")

    def test_cell_distribution(self):
        """Test the main function of the Initial Infected Sweep.
        """
        pop_factory = pe.routine.ToyPopulationFactory()
        pop_params = {"population_size": 100, "cell_number": 5,
                      "microcell_number": 1, "household_number": 1}
        test_population = pop_factory.make_pop(pop_params)
        test_sweep = pe.sweep.InitialInfectedSweep()
        test_sweep.bind_population(test_population)

        # Test that call assigns correct number of infectious people,
        # with all infectious people in one cell
        params = {"simulation_start_time": 0,
                  "initial_infected_number": 4,
                  "initial_infect_cell": True}
        test_sweep(params)
        status = pe.property.InfectionStatus.InfectMild
        num_infectious = []
        for cell in test_population.cells:
            num_infectious.append(sum(cell.compartment_counter
                                  .retrieve()[status]))
        self.assertCountEqual(num_infectious, [4, 0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
