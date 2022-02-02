import unittest

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus


class TestCell(unittest.TestCase):
    """Test the 'Cell' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.cell = pe.Cell()

    def test__init__(self):
        self.assertEqual(self.cell.microcells, [])
        self.assertEqual(self.cell.persons, [])
        self.assertEqual(self.cell.places, [])

    def test_repr(self):
        self.assertEqual(repr(self.cell),
                         "Cell with 0 microcells and 0 people"
                         + " at location (0, 0).")

    def test_cell_location(self):
        local_cell = pe.Cell(loc=(-2, 3.2))
        self.assertEqual(local_cell.location[0], -2)
        self.assertEqual(local_cell.location[1], 3.2)

    def test_add_microcells(self, n=4):
        cell = pe.Cell()
        self.assertEqual(len(cell.microcells), 0)
        cell.add_microcells(n)
        self.assertEqual(len(cell.microcells), n)

    def test_setup(self):
        cell = pe.Cell()
        cell._setup()

    def test_number_infectious(self):
        cell = pe.Cell()
        cell.add_microcells(1)
        cell.microcells[0].add_people(1)
        person = cell.microcells[0].persons[0]
        self.assertEqual(cell.number_infectious(), 0)
        person.update_status(InfectionStatus.InfectMild)
        self.assertEqual(cell.number_infectious(), 1)


if __name__ == '__main__':
    unittest.main()
