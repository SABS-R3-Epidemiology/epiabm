import unittest

import pyEpiabm as pe


class TestCell(unittest.TestCase):
    """Test the 'Cell' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.cell = pe.core.Cell()

    def test__init__(self):
        self.assertEqual(self.cell.microcells, [])
        self.assertEqual(self.cell.persons, [])
        self.assertEqual(self.cell.places, [])

    def test_repr(self):
        self.assertEqual(repr(self.cell),
                         "Cell with 0 microcells and 0 people.")

    def test_add_microcells(self, n=4):
        cell = pe.core.Cell()
        self.assertEqual(len(cell.microcells), 0)
        cell.add_microcells(n)
        self.assertEqual(len(cell.microcells), n)

    def test_setup(self):
        cell = pe.core.Cell()
        cell._setup()


if __name__ == '__main__':
    unittest.main()
