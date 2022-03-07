import unittest
from queue import Queue

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus


class TestCell(unittest.TestCase):
    """Test the 'Cell' class.
    """
    def setUp(self) -> None:
        self.cell = pe.Cell()

    def test__init__(self):
        self.assertEqual(self.cell.location[0], 0)
        self.assertEqual(self.cell.location[1], 0)
        self.assertEqual(self.cell.id, hash(self.cell))
        self.assertEqual(self.cell.microcells, [])
        self.assertEqual(self.cell.persons, [])
        self.assertEqual(self.cell.places, [])
        self.assertIsInstance(self.cell.person_queue, Queue)
        self.assertRaises(ValueError, pe.Cell, (.2, .3, .4))

    def test_repr(self):
        self.assertEqual(repr(self.cell),
                         "Cell with 0 microcells and 0 people"
                         + " at location (0, 0).")

    def test_set_location(self):
        local_cell = pe.Cell(loc=(-2, 3.2))
        self.assertEqual(local_cell.location[0], -2)
        self.assertEqual(local_cell.location[1], 3.2)
        self.assertRaises(ValueError, pe.Cell, (1, 1, 1))
        self.assertRaises(ValueError, pe.Cell, (1, (8, 6)))
        self.assertRaises(ValueError, pe.Cell, ('1', 1))

    def test_set_id(self):
        self.assertEqual(self.cell.id, hash(self.cell))
        self.cell.set_id(2.0)
        self.assertEqual(self.cell.id, 2.0)

    def test_add_microcells(self, n=4):
        self.assertEqual(len(self.cell.microcells), 0)
        self.cell.add_microcells(n)
        self.assertEqual(len(self.cell.microcells), n)

    def test_number_infectious(self):
        self.cell.add_microcells(1)
        self.cell.microcells[0].add_people(1)
        person = self.cell.microcells[0].persons[0]
        self.assertEqual(self.cell.number_infectious(), 0)
        person.update_status(InfectionStatus.InfectMild)
        self.assertEqual(self.cell.number_infectious(), 1)

    def test_set_loc(self):
        self.assertEqual(self.cell.location, (0, 0))
        self.cell.set_location((3.0, 2.0))
        self.assertEqual(self.cell.location, (3.0, 2.0))


if __name__ == '__main__':
    unittest.main()
