import unittest

import pyEpiabm as pe


class TestMicrocell(unittest.TestCase):
    """Test the 'Microcell' class.
    """
    def setUp(self) -> None:
        self.cell = pe.Cell()
        self.microcell = pe.Microcell(self.cell)

    def test__init__(self):
        self.assertEqual(self.microcell.persons, [])
        self.assertEqual(self.microcell.cell, self.cell)
        self.assertEqual(self.microcell.places, [])

    def test_repr(self):
        self.assertEqual(repr(self.microcell),
                         "Microcell with 0 people.")

    def test_set_id(self):
        self.assertEqual(self.microcell.id, hash(self.microcell))
        self.microcell.set_id(2.0)
        self.assertEqual(self.microcell.id, 2.0)

    def test_add_people(self, n=4):
        self.assertEqual(len(self.microcell.persons), 0)
        self.microcell.add_people(n)
        self.assertEqual(len(self.microcell.persons), n)
        self.microcell.add_people(n + 1,
                                  pe.property.InfectionStatus.InfectASympt)
        self.assertEqual(len(self.microcell.persons), 2 * n + 1)
        self.assertEqual(self.cell.number_infectious(), n + 1)

    def test_add_place(self, n=3):
        self.assertEqual(len(self.microcell.places), 0)
        self.microcell.add_place(n, (1.0, 1.0), pe.property.PlaceType.Workplace)
        self.assertEqual(len(self.microcell.places), n)

    def test_setup(self, n=5):
        self.assertEqual(len(self.cell.microcells), 0)
        self.cell.add_microcells(n)
        self.assertEqual(len(self.cell.microcells), n)

    def test_report(self):
        self.microcell.add_people(5)
        self.microcell.notify_person_status_change(
            pe.property.InfectionStatus.Susceptible,
            pe.property.InfectionStatus.Recovered)


if __name__ == '__main__':
    unittest.main()
