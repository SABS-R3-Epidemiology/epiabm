import unittest
from unittest import mock
from queue import Queue

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestHouseholdSweep(TestPyEpiabm):
    """Test the 'HouseholdSweep' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Initialises a population with one infected person. Sets up a
        single household containing this person.

        """
        super(TestHouseholdSweep, cls).setUpClass()
        cls.pop = pe.Population()
        cls.pop.add_cells(1)
        cls.cell = cls.pop.cells[0]
        cls.pop.cells[0].add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.pop.cells[0].microcells[0].add_people(1)
        cls.person = cls.pop.cells[0].microcells[0].persons[0]
        cls.person.infection_status = pe.property.InfectionStatus.InfectMild
        cls.person.secondary_infections_counts = [0]
        cls.house = pe.Household(cls.microcell, [1.0, 1.0])
        cls.house.persons = [cls.person]
        cls.person.household = cls.house
        cls.time = 1
        pe.Parameters.instance().time_steps_per_day = 1

    def test_bind(self):
        self.test_sweep = pe.sweep.HouseholdSweep()
        self.test_sweep.bind_population(self.pop)
        self.assertEqual(self.test_sweep._population.cells[0]
                         .persons[0].infection_status,
                         pe.property.InfectionStatus.InfectMild)

    @mock.patch('pyEpiabm.property.HouseholdInfection.household_foi')
    def test__call__(self, mock_force):
        """Test whether the household sweep function correctly
        adds persons to the queue.

        """
        mock_force.return_value = 100.0

        # Assert a population with one infected will not change the queue
        self.test_sweep = pe.sweep.HouseholdSweep()
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(self.time)
        self.assertTrue(self.cell.person_queue.empty())
        self.assertListEqual(self.person.secondary_infections_counts, [0])

        # Change person's status to recovered
        self.person.infection_status = pe.property.InfectionStatus.Recovered
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(self.time)
        self.assertTrue(self.cell.person_queue.empty())
        self.assertListEqual(self.person.secondary_infections_counts, [0])

        # Add one susceptible to the population, with the mocked infectiousness
        # ensuring they are added to the infected queue.
        self.person.infection_status = pe.property.InfectionStatus.InfectMild
        self.person.set_latent_period(5.0)
        self.person.infection_start_times = [0.0]
        test_queue = Queue()
        new_person = pe.Person(self.microcell)
        new_person.household = self.house
        self.house.persons.append(new_person)
        self.house.susceptible_persons.append(new_person)
        self.pop.cells[0].persons.append(new_person)
        self.assertEqual(new_person.exposure_period, None)
        self.assertEqual(new_person.infector_latent_period, None)

        test_queue.put(new_person)
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(self.time)
        self.assertEqual(self.cell.person_queue.qsize(), 1)
        self.assertListEqual(self.person.secondary_infections_counts, [1])
        self.assertEqual(new_person.exposure_period, 1.0)
        self.assertEqual(new_person.infector_latent_period, 5.0)

        # Change the additional person to recovered, and assert the queue
        # is empty.
        new_person.infection_status = pe.property.InfectionStatus.Recovered
        self.cell.persons.append(new_person)
        self.cell.person_queue = Queue()
        self.house.susceptible_persons.remove(new_person)
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(self.time)
        self.assertTrue(self.cell.person_queue.empty())
        self.assertListEqual(self.person.secondary_infections_counts, [1])
        self.assertEqual(new_person.exposure_period, 1.0)
        self.assertEqual(new_person.infector_latent_period, 5.0)

    def test_no_households(self):
        pop_nh = pe.Population()  # Population without households
        pop_nh.add_cells(1)
        pop_nh.cells[0].add_microcells(1)
        pop_nh.cells[0].microcells[0].add_people(2)
        person_inf = pop_nh.cells[0].microcells[0].persons[0]
        person_inf.infection_status = pe.property.InfectionStatus.InfectMild
        pe.Parameters.instance().time_steps_per_day = 1

        false_sweep = pe.sweep.HouseholdSweep()
        false_sweep.bind_population(pop_nh)
        with self.assertRaises(AttributeError):
            false_sweep(1)


if __name__ == '__main__':
    unittest.main()
