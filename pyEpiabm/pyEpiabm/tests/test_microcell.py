import unittest
import pyEpiabm as pe


class TestMicrocell(unittest.TestCase):
    """Test the 'Microcell' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)

    def test__init__(self):
        self.assertEqual(self.microcell.persons, [])
        self.assertEqual(self.microcell.cell, self.cell)
        self.assertEqual(self.microcell.places, [])

    def test_repr(self):
        self.assertEqual(repr(self.microcell),
                         "Microcell with 0 people.")

    def test_add_people(self, n=4):
        microcell = pe.Microcell(self.cell)
        self.assertEqual(len(microcell.persons), 0)
        microcell.add_people(n)
        self.assertEqual(len(microcell.persons), n)

    def test_add_place(self, n=3):
        microcell = pe.Microcell(self.cell)
        self.assertEqual(len(microcell.places), 0)
        microcell.add_place(n, (1.0, 1.0), pe.PlaceType.Hotel)
        self.assertEqual(len(microcell.places), n)

    def test_setup(self):
        cell = pe.Cell()
        cell.add_microcells(5)
        cell._setup()

    def test_report(self):
        cell = pe.Cell()
        mcell = pe.Microcell(cell)
        mcell.add_people(5)
        cell._setup()
        mcell.notify_person_status_change(
            pe.InfectionStatus.Susceptible,
            pe.InfectionStatus.Recovered)


if __name__ == '__main__':
    unittest.main()
