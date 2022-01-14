import unittest
import pyEpiabm as pe
from queue import Queue
from unittest import mock


class TestPlaceSweep(unittest.TestCase):
    """Test the "PlaceSweep" class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Initialises a population with two people. Sets up a
        single place containing (initially) only one of these people.
        """
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop = cls.pop_factory.make_pop(2, 1, 1, 1, place_number=1)
        cls.cell = cls.pop.cells[0]
        cls.microcell = cls.cell.microcells[0]
        cls.place = cls.cell.places[0]
        cls.person1 = cls.pop.cells[0].microcells[0].persons[0]
        cls.person1.update_status(pe.property.InfectionStatus.InfectMild)
        cls.place.add_person(cls.person1)
        cls.new_person = cls.pop.cells[0].microcells[0].persons[1]
        pe.core.Parameters.instance().time_steps_per_day = 1
        cls.test_sweep = pe.sweep.PlaceSweep()
        cls.test_sweep.bind_population(cls.pop)

    @mock.patch("pyEpiabm.routine.CovidsimHelpers.calc_place_susc")
    @mock.patch("pyEpiabm.routine.CovidsimHelpers.calc_place_inf")
    def test__call__(self, mock_inf, mock_susc):
        """Test whether the place sweep function correctly
        adds persons to the queue, with each infection
        event certain to happen.
        """
        # First test when all persons will be queued.
        mock_inf.return_value = 10
        mock_susc.return_value = 10
        time = 1

        # Assert a population with one infected will not change the queue
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(time)
        self.assertTrue(self.cell.person_queue.empty())

        # Change person"s status to recovered
        self.person1.update_status(pe.property.InfectionStatus.Recovered)
        self.cell.person_queue = Queue()
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(time)
        self.assertTrue(self.cell.person_queue.empty())

        # Add one susceptible to the population, with the mocked infectiousness
        # ensuring they are added to the infected queue.
        self.person1.update_status(pe.property.InfectionStatus.InfectMild)
        self.place.add_person(self.new_person)
        self.cell.person_queue = Queue()
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(time)
        self.assertEqual(self.cell.person_queue.qsize(), 1)

        # Change the additional person to recovered, and assert the queue
        # is empty.
        self.new_person.update_status(pe.property.InfectionStatus.Recovered)
        self.cell.person_queue = Queue()
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(time)
        self.assertTrue(self.cell.person_queue.empty())

        # Now test when binomial dist is activated.
        mock_inf.return_value = 1

        # First, infectee is recovered.
        self.cell.person_queue = Queue()
        self.test_sweep.bind_population(self.pop)
        self.test_sweep(time)
        self.assertTrue(self.cell.person_queue.empty())

        # Change the additional person to susceptible.
        self.new_person.update_status(pe.property.InfectionStatus.Susceptible)
        self.cell.person_queue = Queue()
        self.test_sweep.bind_population(self.pop)
        self.assertTrue(self.cell.person_queue.empty())
        self.test_sweep(time)
        self.assertEqual(self.cell.person_queue.qsize(), 1)


if __name__ == '__main__':
    unittest.main()
