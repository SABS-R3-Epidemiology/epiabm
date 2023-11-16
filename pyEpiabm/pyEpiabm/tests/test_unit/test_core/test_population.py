import unittest

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.mocked_logging_tests import TestMockedLogs


class TestPopulation(TestMockedLogs):
    """Test the 'Population' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestPopulation, cls).setUpClass()  # Sets up patch on logging
        cls.population = pe.Population()

    def test__init__(self):
        self.assertEqual(self.population.cells, [])

    def test_repr(self):
        self.assertEqual(repr(self.population),
                         "Population with 0 cells.")

    def test_add_cells(self, n=4, m=3):
        population = pe.Population()
        self.assertEqual(len(population.cells), 0)

        population.add_cells(n)
        self.assertEqual(len(population.cells), n)
        self.assertEqual(population.cells[-1].id, n-1)

        population.add_cells(m)
        self.assertEqual(len(population.cells), n+m)
        self.assertEqual(population.cells[-1].id, n+m-1)

        # Check all cell IDs are unique
        cell_ids = [cell.id for cell in population.cells]
        self.assertEqual(len(cell_ids), len(set(cell_ids)))

    def test_total_people(self):
        self.assertEqual(self.population.total_people(), 0)


if __name__ == '__main__':
    unittest.main()
