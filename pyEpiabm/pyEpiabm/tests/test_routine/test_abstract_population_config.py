import unittest

from pyEpiabm.routine import AbstractPopulationFactory


class TestPopConfig(unittest.TestCase):
    """Test the 'ToyPopConfig' class.
    """
    def test_make_pop(self):
        """Tests for a make population method.
        """
        with self.assertRaises(NotImplementedError):
            AbstractPopulationFactory.make_pop()


if __name__ == '__main__':
    unittest.main()
