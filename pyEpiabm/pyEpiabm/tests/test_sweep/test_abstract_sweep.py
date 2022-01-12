import unittest
import pyEpiabm as pe


class TestAbstractSweep(unittest.TestCase):
    """Test the 'AbstractSweep' class.
    """

    def test_construct(self):
        pe.AbstractSweep()

    def test_bind_population(self):
        subject = pe.AbstractSweep()
        population = pe.Population()
        subject.bind_population(population)

    def test___call__(self):
        subject = pe.AbstractSweep()
        self.assertRaises(NotImplementedError, subject.__call__, 1)


if __name__ == '__main__':
    unittest.main()
