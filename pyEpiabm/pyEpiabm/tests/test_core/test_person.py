import unittest

import pyEpiabm as pe


class TestPerson(unittest.TestCase):
    """Test the 'Person' class.
    """
    def setUp(self) -> None:
        self.cell = pe.Cell()
        self.cell.add_microcells(1)
        self.microcell = self.cell.microcells[0]
        self.microcell.add_people(1)
        self.person = self.microcell.persons[0]

    def test__init__(self):
        self.assertEqual(self.person.age, 0)
        self.assertEqual(self.person.infectiousness, 0)
        self.assertEqual(self.person.microcell, self.microcell)

    def test_repr(self):
        self.assertEqual(repr(self.person), "Person, Age = 0.")

    def test_is_infectious(self):
        self.assertFalse(self.person.is_infectious())
        self.person.update_status(pe.property.InfectionStatus.InfectMild)
        self.assertTrue(self.person.is_infectious())

    def test_is_susceptible(self):
        self.person.update_status(pe.property.InfectionStatus.Susceptible)
        self.assertTrue(self.person.is_susceptible())
        self.person.update_status(pe.property.InfectionStatus.InfectMild)
        self.assertFalse(self.person.is_susceptible())

    def test_update_status(self):
        self.person.update_status(pe.property.InfectionStatus.InfectMild)
        self.assertEqual(
            self.person.infection_status,
            pe.property.InfectionStatus.InfectMild)

    def test_update_time(self):
        self.assertIsNone(self.person.time_of_status_change)
        self.person.update_time_to_status_change()
        self.assertTrue(1 <= self.person.time_of_status_change
                        <= 10)

    def test_configure_place(self):
        # Tests both the add and remove functions
        self.assertEqual(len(self.person.places), 0)
        test_place = pe.Place((1.0, 1.0), pe.property.PlaceType.Workplace,
                              self.cell, self.microcell)
        self.person.add_place(test_place)
        self.assertTrue(len(self.person.places) > 0)
        test_cell = pe.Cell
        test_place_2 = pe.Place((1.0, 1.0), pe.property.PlaceType.Workplace,
                                test_cell, pe.Microcell(test_cell))
        self.assertRaises(AttributeError, self.person.add_place, test_place_2)

        self.person.remove_place(test_place)
        self.assertEqual(len(self.person.places), 0)
        self.assertRaises(KeyError, self.person.remove_place, test_place_2)


if __name__ == '__main__':
    unittest.main()
