import unittest
import pyEpiabm as pe


class TestPlace(unittest.TestCase):
    '''Test the place class.
    '''
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
        self.assertRaises(KeyError,  pe.Place, (1, 1), pe.PlaceType.Hotel,
                          self.cell, pe.Microcell)
        self.place = pe.Place((1, 1), pe.PlaceType.Hotel, self.cell,
                              self.microcell)
        self.assertEqual(len(self.place.persons), 0)

    def test_change_persons(self):
        '''Tests the add and remove persons functions'''
        self.place = pe.Place((1, 1), pe.PlaceType.Hotel, self.cell,
                              self.microcell)
        self.place.add_person(self.person)
        self.assertEqual(len(self.place.persons), 1)

        self.place.remove_person(self.person)
        self.assertEqual(len(self.place.persons), 0)
        self.assertRaises(KeyError, self.place.remove_person, self.person)


if __name__ == '__main__':
    unittest.main()
