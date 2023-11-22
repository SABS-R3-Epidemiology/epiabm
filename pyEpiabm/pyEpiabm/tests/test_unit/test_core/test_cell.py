import unittest
from queue import Queue

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestCell(TestPyEpiabm):
    """Test the 'Cell' class.
    """
    def setUp(self) -> None:
        self.cell = pe.Cell()

    def test__init__(self):
        self.assertEqual(self.cell.location[0], 0)
        self.assertEqual(self.cell.location[1], 0)
        self.assertEqual(self.cell.id, str(hash(self.cell)))
        self.assertEqual(self.cell.microcells, [])
        self.assertEqual(self.cell.persons, [])
        self.assertEqual(self.cell.places, [])
        self.assertIsInstance(self.cell.person_queue, Queue)
        self.assertIsInstance(self.cell.PCR_queue, Queue)
        self.assertIsInstance(self.cell.LFT_queue, Queue)
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
        cells = []
        cell1 = pe.Cell()
        self.assertEqual(self.cell.id, str(hash(self.cell)))
        self.assertRaises(TypeError, self.cell.set_id, id=2.0, cells=[cell1])
        self.assertRaises(ValueError, self.cell.set_id, id="2.0", cells=[cell1])
        self.cell.set_id(id="2", cells=[cell1])
        self.assertEqual(self.cell.id, "2")
        cell1.set_id(id="1", cells=[cell1])
        cells.append(cell1)
        new_cell = pe.Cell((1,1))
        cells.append(new_cell)
        self.assertRaises(ValueError, new_cell.set_id, id="1", cells=[cell1])

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
        person.update_status(InfectionStatus.InfectICU)
        self.assertEqual(self.cell.number_infectious(), 1)
        person.update_status(InfectionStatus.Recovered)
        self.assertEqual(self.cell.number_infectious(), 0)

    def test_set_loc(self):
        self.assertEqual(self.cell.location, (0, 0))
        self.cell.set_location((3.0, 2.0))
        self.assertEqual(self.cell.location, (3.0, 2.0))

    def test_testing_queue(self):
        self.cell.add_microcells(1)
        self.cell.microcells[0].add_people(1)
        person = self.cell.microcells[0].persons[0]
        self.cell.enqueue_PCR_testing(person)
        self.cell.enqueue_LFT_testing(person)

        self.assertEqual(self.cell.PCR_queue.qsize(), 1)
        self.assertEqual(self.cell.LFT_queue.qsize(), 1)


if __name__ == '__main__':
    unittest.main()
