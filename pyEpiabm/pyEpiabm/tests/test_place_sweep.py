import unittest
import pyEpiabm as pe
from queue import Queue
from unittest import mock


class TestPlaceSweep(unittest.TestCase):
    """Test the "PlaceSweep" class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Initialises a population with one infected person. Sets up a
        single place containing this person.
        """
        cls.pop_factory = pe.ToyPopulationFactory()
        cls.pop = cls.pop_factory.make_pop(1, 1, 1, 1, place_number=1)
        cls.cell = cls.pop.cells[0]
        cls.microcell = cls.cell.microcells[0]
        cls.place = cls.cell.places[0]
        cls.person1 = cls.pop.cells[0].microcells[0].persons[0]
        pe.Parameters.instance().time_steps_per_day = 1

    @mock.patch("pyEpiabm.CovidsimHelpers.calc_place_susc")
    @mock.patch("pyEpiabm.CovidsimHelpers.calc_place_inf")
    def test__call__(self, mock_inf, mock_susc):
        """Test whether the place sweep function correctly
        adds persons to the queue, with each infection
        event certain to happen.
        """
        mock_inf.return_value = 10
        mock_susc.return_value = 10
        subject = pe.PlaceSweep()
        subject.bind_population(self.pop)
        time = 1

        # Assert a population with one infected will not change the queue
        subject(time)
        self.assertTrue(self.cell.person_queue.empty())

        # Change person"s status to recovered
        self.person1.infection_status = pe.InfectionStatus.Recovered
        subject.bind_population(self.pop)
        subject(time)
        self.assertTrue(self.cell.person_queue.empty())

        # Add one susceptible to the population, with the mocked infectiousness
        # ensuring they are added to the infected queue.
        self.person1.infection_status = pe.InfectionStatus.InfectMild
        test_queue = Queue()
        new_person = pe.Person(self.microcell)
        self.place.persons.append(new_person)
        self.pop.cells[0].persons.append(new_person)

        test_queue.put(new_person)
        subject.bind_population(self.pop)
        subject(time)
        self.assertEqual(self.cell.person_queue.qsize(), 1)

        # Change the additional person to recovered, and assert the queue
        # is empty.
        new_person.infection_status = pe.InfectionStatus.Recovered
        self.cell.persons.append(new_person)
        self.cell.person_queue = Queue()
        subject.bind_population(self.pop)
        subject(time)
        self.assertTrue(self.cell.person_queue.empty())

    @mock.patch("pyEpiabm.CovidsimHelpers.calc_place_susc")
    @mock.patch("pyEpiabm.CovidsimHelpers.calc_place_inf")
    def test__call__2(self, mock_inf, mock_susc):
        """Test whether the place sweep function correctly
        adds persons to the queue, with each infection
        event certain NOT to happen.
        """
        mock_inf.return_value = 0
        mock_susc.return_value = 10
        subject = pe.PlaceSweep()
        subject.bind_population(self.pop)
        time = 1

        # One infected and one susceptible in the population, with the
        # mocked infectiousness ensuring no change to the infected queue.
        self.person1.infection_status = pe.InfectionStatus.InfectMild
        test_queue = Queue()
        new_person = pe.Person(self.microcell)
        self.place.persons.append(new_person)
        self.pop.cells[0].persons.append(new_person)

        test_queue.put(new_person)
        subject.bind_population(self.pop)
        subject(time)
        self.assertTrue(self.cell.person_queue.empty())

        # Change the additional person to recovered, and assert the queue
        # is empty.
        mock_inf.return_value = .9
        new_person.infection_status = pe.InfectionStatus.Recovered
        self.cell.person_queue = Queue()
        subject.bind_population(self.pop)
        subject(time)
        self.assertTrue(self.cell.person_queue.empty())


if __name__ == '__main__':
    unittest.main()
