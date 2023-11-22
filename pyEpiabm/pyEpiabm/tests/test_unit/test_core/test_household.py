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
        cls.pop.add_cells(2)
        cls.cell = cls.pop.cells[0]
        cls.cell_other = cls.pop.cells[1]
        cls.pop.cells[0].add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.pop.cells[0].microcells[0].add_people(1)
        cls.person = cls.pop.cells[0].microcells[0].persons[0]

    def test_construct(self):
        pe.Household(self.microcell, (1, 1))

    def test___repr__(self):
        subject = pe.Household(self.microcell, (1, 1))
        self.assertIsInstance(repr(subject), str)
        test_string = "Household at (1.00, 1.00) with 0 people."
        self.assertEqual(repr(subject), test_string)

    def test_location_type(self):
        self.assertRaises(ValueError, pe.Household,
                          self.microcell, (1, 1, 1))
        self.assertRaises(ValueError, pe.Household,
                          self.microcell, (1, (8, 6)))
        self.assertRaises(ValueError, pe.Household,
                          self.microcell, ('1', 1))

    def test_add_susceptible_person(self):
        subject = pe.Household(self.microcell, (1, 1))
        self.assertEqual(len(subject.susceptible_persons), 0)
        self.assertEqual(subject.susceptible_persons, [])
        subject.add_susceptible_person(self.person)
        self.assertEqual(len(subject.susceptible_persons), 1)
        self.assertEqual(subject.susceptible_persons, [self.person])

    def test_remove_susceptible_person(self):
        subject = pe.Household(self.microcell, (1, 1))
        subject.susceptible_persons.append(self.person)
        self.assertEqual(len(subject.susceptible_persons), 1)
        self.assertEqual(subject.susceptible_persons, [self.person])
        subject.remove_susceptible_person(self.person)
        self.assertEqual(len(subject.susceptible_persons), 0)
        self.assertEqual(subject.susceptible_persons, [])

    def test_set_id(self):
        subject = pe.Household(self.microcell, (1, 1))
        init_id = str(self.microcell.id) + "." + \
                  str(len(self.microcell.households)-1)
        self.assertEqual(subject.id, init_id)
        subject.set_id("0.0.0")
        self.assertEqual(subject.id, "0.0.0")
        subject.set_id("10.7.20")
        self.assertEqual(subject.id, "10.7.20")
        self.assertRaises(TypeError, subject.set_id, 2.0)
        self.assertRaises(ValueError, subject.set_id, "a.b.c")
        self.assertRaises(ValueError, subject.set_id, "0.0.")
        self.assertRaises(ValueError, subject.set_id, "0.0.0.0")


if __name__ == '__main__':
    unittest.main()
