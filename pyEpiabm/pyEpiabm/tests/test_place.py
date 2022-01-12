import unittest
import pyEpiabm as pe


class TestPlace(unittest.TestCase):
    """Test the 'Place' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
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
        test_place = pe.Place((1.0, 1.0), pe.PlaceType.Hotel, self.cell,
                              self.microcell)
        self.assertEqual(test_place._location, (1.0, 1.0))
        self.assertEqual(test_place.persons, [])
        self.assertEqual(test_place.place_type, pe.PlaceType.Hotel)
        self.assertEqual(test_place.max_capacity, 50)
        self.assertEqual(test_place.susceptibility, 0)
        self.assertEqual(test_place.infectiveness, 0)
        new_cell = pe.Cell()
        self.assertRaises(KeyError, pe.Place, (1, 1), pe.PlaceType.Hotel,
                          new_cell, self.microcell)

        self.assertEqual(len(test_place.persons), 0)

    def test_change_persons(self):
        """Tests the add and remove person functions.
        """
        test_place = pe.Place((1, 1), pe.PlaceType.Hotel, self.cell,
                              self.microcell)
        test_place.add_person(self.person)
        self.assertEqual(len(test_place.persons), 1)

        test_place.remove_person(self.person)
        self.assertEqual(len(test_place.persons), 0)
        self.assertRaises(KeyError, test_place.remove_person, self.person)

        test_place.add_person(self.person)
        test_place.add_person(pe.Person(self.microcell))
        self.assertEqual(len(test_place.persons), 2)
        test_place.empty_place()
        print(test_place.persons)
        self.assertEqual(len(test_place.persons), 0)

    def test_set_susc(self):
        test_place = pe.Place((1, 1), pe.PlaceType.Hotel, self.cell,
                              self.microcell)
        self.assertEqual(test_place.susceptibility, 0)
        test_place.set_susceptibility(10)
        self.assertEqual(test_place.susceptibility, 10)

    def test_set_inf(self):
        test_place = pe.Place((1, 1), pe.PlaceType.Hotel, self.cell,
                              self.microcell)
        self.assertEqual(test_place.infectiveness, 0)
        test_place.set_infectiveness(10)
        self.assertEqual(test_place.infectiveness, 10)

    def test_set_max_cap(self):
        test_place = pe.Place((1, 1), pe.PlaceType.Hotel, self.cell,
                              self.microcell)
        self.assertEqual(test_place.max_capacity, 50)
        test_place.set_max_cap(10)
        self.assertEqual(test_place.max_capacity, 10)


if __name__ == "__main__":
    unittest.main()
