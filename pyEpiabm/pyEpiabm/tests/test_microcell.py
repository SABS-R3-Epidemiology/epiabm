import unittest
import pyEpiabm as pe


class TestMicrocell(unittest.TestCase):
    """
    Test the 'Microcell' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)

    def test__init__(self):
        self.assertEqual(self.microcell.persons, [])
        self.assertEqual(self.microcell.cell, self.cell)

    def test_repr(self):
        self.assertEqual(repr(self.microcell),
                         "Microcell with 0 people")

    def test_add_people(self, n=4):
        cell = pe.Cell()
        microcell = pe.Microcell(cell)
        self.assertEqual(len(microcell.persons), 0)
        microcell.add_people(n)
        self.assertEqual(len(microcell.persons), n)


if __name__ == '__main__':
    unittest.main()
