import unittest

import pyEpiabm as pe
from pyEpiabm.property import PlaceType
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestPlace(TestPyEpiabm):
    """Test the 'Place' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestPlace, cls).setUpClass()  # Sets up parameters
        cls.pop = pe.Population()
        cls.pop.add_cells(1)
        cls.cell = cls.pop.cells[0]
        cls.pop.cells[0].add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.pop.cells[0].microcells[0].add_people(1)
        cls.person = cls.pop.cells[0].microcells[0].persons[0]

    def test_construct(self):
        """Tests constructor method.
        """
        test_place = pe.Place((1.0, 1.0), PlaceType.Workplace,
                              self.cell, self.microcell)
        self.assertEqual(test_place._location, (1.0, 1.0))
        self.assertEqual(test_place.persons, [])
        self.assertEqual(test_place.place_type, PlaceType.Workplace)
        self.assertDictEqual(test_place.person_groups, {0: []})
        self.assertEqual(test_place.susceptibility, 0)
        self.assertEqual(test_place.infectiousness, 0)
        new_cell = pe.Cell()
        self.assertRaises(KeyError, pe.Place, (1.0, 1.0),
                          PlaceType.Workplace, new_cell,
                          self.microcell)

        self.assertEqual(len(test_place.persons), 0)

    def test_repr(self):
        test_place = pe.Place((1.0, 1.0), PlaceType.Workplace,
                              self.cell, self.microcell)
        self.assertEqual(repr(test_place),
                         "Place of type PlaceType.Workplace at location "
                         "(1.0, 1.0), with current occupancy 0.")

    def test_change_persons(self):
        """Tests the add and remove person functions.
        """
        test_place = pe.Place((1.0, 1.0), pe.property.PlaceType.Workplace,
                              self.cell, self.microcell)
        test_place.add_person(self.person)
        self.assertEqual(len(self.person.places), 1)
        self.assertDictEqual(test_place.person_groups, {0: [self.person]})
        self.assertEqual(len(test_place.persons), 1)
        self.assertEqual(test_place.get_group_index(self.person), 0)

        test_place.remove_person(self.person)
        self.assertDictEqual(test_place.person_groups, {0: []})
        self.assertEqual(len(test_place.persons), 0)
        self.assertRaises(KeyError, test_place.remove_person, self.person)

        test_place.add_person(self.person, person_group=1)
        self.assertEqual(test_place.get_group_index(self.person), 1)
        test_place.add_person(pe.Person(self.microcell))
        self.assertEqual(len(test_place.persons), 2)
        test_place.empty_place([0, 1])
        self.assertEqual(len(test_place.persons), 0)
        test_place.empty_place([4])
        self.assertEqual(len(test_place.persons), 0)
        self.assertRaises(KeyError, test_place.get_group_index, self.person)

    def test_set_susc(self):
        test_place = pe.Place((1.0, 1.0), pe.property.PlaceType.Workplace,
                              self.cell, self.microcell)
        self.assertEqual(test_place.susceptibility, 0)
        test_place.set_susceptibility(10)
        self.assertEqual(test_place.susceptibility, 10)

    def test_set_inf(self):
        test_place = pe.Place((1.0, 1.0), pe.property.PlaceType.Workplace,
                              self.cell, self.microcell)
        self.assertEqual(test_place.infectiousness, 0)
        test_place.set_infectiousness(10)
        self.assertEqual(test_place.infectiousness, 10)

    def test_location_type(self):
        self.assertRaises(ValueError, pe.Place, (1.0, 1.0, 1.0),
                          pe.property.PlaceType.Workplace,
                          self.cell, self.microcell)
        self.assertRaises(ValueError, pe.Place, (1.0, '8.0'),
                          pe.property.PlaceType.Workplace,
                          self.cell, self.microcell)
        self.assertRaises(ValueError, pe.Place, ([3], 1.0),
                          pe.property.PlaceType.Workplace,
                          self.cell, self.microcell)


if __name__ == "__main__":
    unittest.main()
