import unittest

import pyEpiabm as pe
from pyEpiabm.tests.parameter_config_tests import TestPyEpiabm


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
        num_infectious = self.cell.compartment_counter.retrieve()[status]
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
                  "initial_infected_cell": True}
        test_sweep(params)
        status = pe.property.InfectionStatus.InfectMild
        num_infectious = []
        for cell in test_population.cells:
            num_infectious.append(cell.compartment_counter
                                  .retrieve()[status])
        self.assertCountEqual(num_infectious, [4, 0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
