import unittest
import pyEpiabm as pe
from queue import Queue
from unittest import mock


class TestUpdatePlaceSweep(unittest.TestCase):
    """Test the "UpdatePlaceSweep" class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """ Initialises a population with one infected person. Sets up a
        single household containing this person.
        """
        cls.pop = pe.Population()
        cls.pop.add_cells(1)
        cls.cell = cls.pop.cells[0]
        cls.pop.cells[0].add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.pop.cells[0].microcells[0].add_people(1)
        cls.person = cls.pop.cells[0].microcells[0].persons[0]
        cls.person.infection_status = pe.InfectionStatus.InfectMild
        cls.microcell.add_place(1, (1, 1), pe.PlaceType.Hotel, 100)
        cls.place = cls.cell.places[0]
        pe.Parameters.instance().time_steps_per_day = 1
        cls.time = 1

    def test_bind(self):
        self.test_sweep = pe.UpdatePlaceSweep()
        self.test_sweep.bind_population(self.pop)
        self.assertEqual(self.place.place_type, pe.PlaceType.Hotel)

    @mock.patch("pyEpiabm.CovidsimHelpers.calc_place_susc")
    @mock.patch("pyEpiabm.CovidsimHelpers.calc_place_inf")
    def test__call__(self, mock_inf, mock_susc):
        """
        Test whether the household sweep function correctly
        adds persons to the queue.
        """
        mock_inf.return_value = 10
        mock_susc.return_value = 10
        self.assertTrue(self.place.persons.empty

        cls.place.add_person(cls.person)
        self.test_sweep(self.time)


if __name__ == "__main__":
    unittest.main()
