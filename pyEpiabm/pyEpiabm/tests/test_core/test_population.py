import unittest
import pyEpiabm as pe


class TestPopulation(unittest.TestCase):
    """Test the 'Population' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.population = pe.core.Population()

    def test__init__(self):
        self.assertEqual(self.population.cells, [])

    def test_repr(self):
        self.assertEqual(repr(self.population),
                         "Population with 0 cells.")

    def test_add_cells(self, n=4):
        population = pe.core.Population()
        self.assertEqual(len(population.cells), 0)
        population.add_cells(n)
        self.assertEqual(len(population.cells), n)

    def test_setup(self):
        population = pe.core.Population()
        population.add_cells(5)
        population.setup()

    def test_total_people(self):
        self.assertEqual(self.population.total_people(), 0)


if __name__ == '__main__':
    unittest.main()
