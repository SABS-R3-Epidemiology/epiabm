import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.core import Parameters
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestQueueSweep(TestPyEpiabm):
    """Test the 'QueueSweep' class.
    """
    def setUp(self) -> None:
        """Sets up a population we can use throughout the test.
        2 people are located in one microcell.
        """
        self.pop_factory = pe.routine.ToyPopulationFactory()
        self.pop_params = {"population_size": 2, "cell_number": 1,
                           "microcell_number": 1, "household_number": 1}
        self.test_population = self.pop_factory.make_pop(self.pop_params)

        self.cell = self.test_population.cells[0]
        self.person1 = self.test_population.cells[0].microcells[0].persons[0]
        self.person1.infection_status = pe.property.InfectionStatus.InfectMild
        self.person2 = self.test_population.cells[0].microcells[0].persons[1]

        self.time = 1

    def test_bind(self):
        """Test population binds correctly.
        """
        self.test_sweep = pe.sweep.QueueSweep()
        self.test_sweep.bind_population(self.test_population)
        self.assertEqual(self.test_sweep._population.cells[0]
                         .persons[0].infection_status,
                         pe.property.InfectionStatus.InfectMild)

    def test_call(self):
        """Test the main function of the Queue Sweep.
        Person 2 is enqueued.
        Checks the population updates as expected.
        """
        self.cell.enqueue_person(self.person2)
        test_sweep = pe.sweep.QueueSweep()
        test_sweep.bind_population(self.test_population)
        # Test that the queue has one person
        self.assertFalse(self.cell.person_queue.empty())

        # Run the Queue Sweep.
        test_sweep(self.time)

        # Check queue is cleared.
        self.assertTrue(self.cell.person_queue.empty())
        # Check person 2 current infection status
        self.assertEqual(self.person2.infection_status,
                         pe.property.InfectionStatus.Susceptible)
        # Check person 2 has updated next infection status
        self.assertEqual(self.person2.next_infection_status,
                         pe.property.InfectionStatus.Exposed)
        # Check person 2 has updated time
        self.assertEqual(self.person2.time_of_status_change,
                         self.time)

    def test_vaccine_protection_full(self):
        """Tests that a vaccinated person will be moved to the vaccinated
        compartment.
        """
        self.person2.is_vaccinated = True
        self.person2.date_vaccinated = 0
        self.cell.enqueue_person(self.person2)

        test_sweep = pe.sweep.QueueSweep()
        test_sweep.bind_population(self.test_population)
        # Test that the queue has one person
        self.assertFalse(self.cell.person_queue.empty())

        # Run the Queue Sweep.
        test_sweep(self.time)

        # Check queue is cleared.
        self.assertTrue(self.cell.person_queue.empty())
        # Check person 2 current infection status
        self.assertEqual(self.person2.infection_status,
                         pe.property.InfectionStatus.Susceptible)
        # Check person 2 has updated next infection status
        self.assertEqual(self.person2.next_infection_status,
                         pe.property.InfectionStatus.Vaccinated)
        # Check person 2 has updated time
        self.assertEqual(self.person2.time_of_status_change,
                         self.time)

    @mock.patch('pyEpiabm.Parameters.instance')
    def test_vaccine_protection_partial(self, mock_params):
        """Tests that a vaccinated person will become infected if the vaccine
        is not effective.
        """
        mock_params.return_value.\
            intervention_params = {'vaccine_params': {'time_to_efficacy': 0,
                                                      'vacc_protectiveness': 0}
                                   }
        self.person2.is_vaccinated = True
        self.person2.date_vaccinated = 0
        self.cell.enqueue_person(self.person2)

        test_sweep = pe.sweep.QueueSweep()
        test_sweep.bind_population(self.test_population)
        # Test that the queue has one person
        self.assertFalse(self.cell.person_queue.empty())

        # Run the Queue Sweep.
        test_sweep(self.time)

        # Check queue is cleared.
        self.assertTrue(self.cell.person_queue.empty())
        # Check person 2 current infection status
        self.assertEqual(self.person2.infection_status,
                         pe.property.InfectionStatus.Susceptible)
        # Check person 2 has updated next infection status
        self.assertEqual(self.person2.next_infection_status,
                         pe.property.InfectionStatus.Exposed)
        # Check person 2 has updated time
        self.assertEqual(self.person2.time_of_status_change,
                         self.time)

    @mock.patch('pyEpiabm.Parameters.instance')
    def test_vaccine_protection_time(self, mock_params):
        """Tests that a vaccinated person will become infected if the vaccine
        time to efficacy has not yet passes.
        """
        mock_params.return_value.\
            intervention_params = {'vaccine_params': {'time_to_efficacy': 14,
                                                      'vacc_protectiveness': 1}
                                   }
        self.person2.is_vaccinated = True
        self.person2.date_vaccinated = 0
        self.cell.enqueue_person(self.person2)

        test_sweep = pe.sweep.QueueSweep()
        test_sweep.bind_population(self.test_population)
        # Test that the queue has one person
        self.assertFalse(self.cell.person_queue.empty())

        # Run the Queue Sweep.
        test_sweep(self.time)

        # Check queue is cleared.
        self.assertTrue(self.cell.person_queue.empty())
        # Check person 2 current infection status
        self.assertEqual(self.person2.infection_status,
                         pe.property.InfectionStatus.Susceptible)
        # Check person 2 has updated next infection status
        self.assertEqual(self.person2.next_infection_status,
                         pe.property.InfectionStatus.Exposed)
        # Check person 2 has updated time
        self.assertEqual(self.person2.time_of_status_change,
                         self.time)


if __name__ == '__main__':
    unittest.main()
