import unittest
import pyEpiabm as pe


class TestPopulation(unittest.TestCase):
    """Test the 'Population' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.population = pe.Population()

    def test__init__(self):
        self.assertEqual(self.population.cells, [])

    def test_repr(self):
        self.assertEqual(repr(self.population),
                         "Population with 0 cells.")

    def test_add_cells(self, n=4):
        population = pe.Population()
        self.assertEqual(len(population.cells), 0)
        population.add_cells(n)
        self.assertEqual(len(population.cells), n)
    
    def test_setup(self):
        population = pe.Population()
        population.add_cells(5)
        population.setup()


if __name__ == '__main__':
    unittest.main()
