import unittest
from unittest import mock
from queue import Queue

import pyEpiabm as pe
from pyEpiabm.sweep import HouseholdSweep


class TestHouseholdSweep(unittest.TestCase):
    """Test the 'HouseholdSweep' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Initialises a population with one infected person. Sets up a
        single household containing this person.
        """
        cls.pop = pe.Population()
        cls.house = pe.Household([1.0, 1.0])
        cls.pop.add_cells(1)
        cls.cell = cls.pop.cells[0]
        cls.pop.cells[0].add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.pop.cells[0].microcells[0].add_people(1)
        cls.person = cls.pop.cells[0].microcells[0].persons[0]
        cls.person.infection_status = pe.InfectionStatus.InfectMild
        cls.person.household = cls.house
        cls.house.persons = [cls.person]
        cls.time = 1
        pe.Parameters.instance().time_steps_per_day = 1

    def test_bind(self):
        self.test_sweep = HouseholdSweep()
        self.test_sweep.bind_population(self.pop)
        self.assertEqual(self.test_sweep._population.cells[0]
                         .persons[0].infection_status,
                         pe.InfectionStatus.InfectMild)

    @mock.patch('pyEpiabm.CovidsimHelpers.calc_house_susc')
    @mock.patch('pyEpiabm.CovidsimHelpers.calc_house_inf')
    def test__call__(self, mock_inf, mock_susc):
        """Test whether the household sweep function correctly
        adds persons to the queue.
        """
        mock_inf.return_value = 10.0
        mock_susc.return_value = 10.0

        # Assert a population with one infected will not change the queue
        self.test_sweep = HouseholdSweep()
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(self.time)
        self.assertTrue(self.cell.person_queue.empty())

        # Change person's status to recovered
        self.person.infection_status = pe.InfectionStatus.Recovered
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(self.time)
        self.assertTrue(self.cell.person_queue.empty())

        # Add one susceptible to the population, with the mocked infectiousness
        # ensuring they are added to the infected queue.
        self.person.infection_status = pe.InfectionStatus.InfectMild
        test_queue = Queue()
        new_person = pe.Person(self.microcell)
        new_person.household = self.house
        self.house.persons.append(new_person)
        self.pop.cells[0].persons.append(new_person)

        test_queue.put(new_person)
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(self.time)
        self.assertEqual(self.cell.person_queue.qsize(), 1)

        # Change the additional person to recovered, and assert the queue
        # is empty.
        new_person.infection_status = pe.InfectionStatus.Recovered
        self.cell.persons.append(new_person)
        self.cell.person_queue = Queue()
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(self.time)
        self.assertTrue(self.cell.person_queue.empty())


if __name__ == '__main__':
    unittest.main()
