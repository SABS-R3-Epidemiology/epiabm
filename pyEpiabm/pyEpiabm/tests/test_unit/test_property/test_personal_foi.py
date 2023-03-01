import unittest

import pyEpiabm as pe
from pyEpiabm.property import PersonalInfection
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestPersonalInfection(TestPyEpiabm):
    """Test the 'PersonalInfection' class, which contains the
    infectiousness and susceptibility calculations to
    determine whether infection events occur between individuals.
    Each function should return a number greater than 0.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        super(TestPersonalInfection, cls).setUpClass()  # Sets up parameters
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)
        cls.infector = pe.Person(cls.microcell)
        cls.infector.infectiousness = 1.0
        cls.infectee = pe.Person(cls.microcell)
        cls.time = 1

    def test_person_inf(self):
        result = PersonalInfection.person_inf(self.infector, self.time)
        self.assertEqual(result, 1.0)
        self.assertIsInstance(result, float)

    def test_person_susc(self):
        result = PersonalInfection.person_susc(self.infector,
                                               self.infectee,
                                               self.time)
        self.assertEqual(result, 1.0)
        self.assertIsInstance(result, float)


if __name__ == '__main__':
    unittest.main()
