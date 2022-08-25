import unittest

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestHousehold(TestPyEpiabm):
    """Test the 'Household' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestHousehold, cls).setUpClass()  # Sets up parameters
        cls.pop = pe.Population()
        cls.pop.add_cells(1)
        cls.cell = cls.pop.cells[0]
        cls.pop.cells[0].add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.pop.cells[0].microcells[0].add_people(1)
        cls.person = cls.pop.cells[0].microcells[0].persons[0]

    def test_construct(self):
        pe.Household(self.cell, self.microcell, (1, 1))

    def test___repr__(self):
        subject = pe.Household(self.cell, self.microcell, (1, 1))
        self.assertIsInstance(repr(subject), str)
        test_string = "Household at (1.00, 1.00) with 0 people."
        self.assertEqual(repr(subject), test_string)

    def test_location_type(self):
        self.assertRaises(ValueError, pe.Household,
                          self.cell, self.microcell, (1, 1, 1))
        self.assertRaises(ValueError, pe.Household,
                          self.cell, self.microcell, (1, (8, 6)))
        self.assertRaises(ValueError, pe.Household,
                          self.cell, self.microcell, ('1', 1))


if __name__ == '__main__':
    unittest.main()
