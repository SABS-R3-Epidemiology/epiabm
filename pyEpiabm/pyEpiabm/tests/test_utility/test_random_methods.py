import unittest

from pyEpiabm.utility import RandomMethods


class TestInfectionStatus(unittest.TestCase):
    """Test the 'RandomMethods' class.
    """

    def test_randum_number(self):
        number = RandomMethods.random_number()
        self.assertTrue(number >= 0)


if __name__ == '__main__':
    unittest.main()
