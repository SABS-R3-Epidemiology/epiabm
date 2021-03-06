import unittest

import pyEpiabm as pe
from pyEpiabm.property import PlaceInfection
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestPlaceInfection(TestPyEpiabm):
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
        super(TestPlaceInfection, cls).setUpClass()  # Sets up parameters
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)
        cls.infector = pe.Person(cls.microcell)
        cls.infector.infectiousness = 1.0
        cls.infectee = pe.Person(cls.microcell)
        cls.place = pe.Place((1, 1), pe.property.PlaceType.Workplace,
                             cls.cell, cls.microcell)
        cls.place.add_person(cls.infector)
        cls.place.add_person(cls.infectee)
        cls.time = 1.0

    def test_place_susc(self):
        result = PlaceInfection.place_susc(self.place, self.infector,
                                           self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_place_inf(self):
        result = PlaceInfection.place_inf(self.place, self.infector, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

        # Parameter free test
        place = pe.Place((1, 1), pe.property.PlaceType.OutdoorSpace,
                         self.cell, self.microcell)
        result = PlaceInfection.place_inf(place, self.infector, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_place_foi(self):
        result = PlaceInfection.place_foi(self.place, self.infector,
                                          self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)


if __name__ == '__main__':
    unittest.main()
