import unittest

import pyEpiabm as pe
from pyEpiabm.property import PlaceInfection


class TestPlaceInfection(unittest.TestCase):
    """Test the 'PlaceInfection' class, which contains the
    infectiousness and susceptibility calculations that
    determine whether infection events occur within places.
    Each function should return a number greater than 0.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)
        cls.infector = pe.Person(cls.microcell)
        cls.infectee = pe.Person(cls.microcell)
        cls.place = pe.Place((1, 1), pe.property.PlaceType.Hotel,
                             cls.cell, cls.microcell)
        cls.place.add_person(cls.infector)
        cls.place.add_person(cls.infectee)
        cls.timestep = 1

    def test_place_susc(self):
        result = PlaceInfection.place_susc(self.place, self.infector,
                                           self.infectee, self.timestep)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_place_inf(self):
        result = PlaceInfection.place_inf(self.place, self.timestep)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_place_foi(self):
        result = PlaceInfection.place_foi(self.place, self.infector,
                                          self.infectee, self.timestep)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)


if __name__ == '__main__':
    unittest.main()
