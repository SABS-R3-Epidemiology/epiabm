import unittest
import pyEpiabm as pe


class TestHouseholdSweep(unittest.TestCase):
    """
    Test the 'HouseholdSweep' class.
    """

    def test_construct(self):
        pe.HouseholdSweep()

    def test_bind_population(self):
        subject = pe.HouseholdSweep()
        population = pe.Population()
        subject.bind_population(population)

    def test___call__(self):
        subject = pe.HouseholdSweep()
        self.assertRaises(NotImplementedError, subject.__call__, 1)


if __name__ == '__main__':
    unittest.main()
