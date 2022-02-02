import unittest

from pyEpiabm.utility import DistanceFunctions


class TestDistanceFunctions(unittest.TestCase):
    """Test the 'DistanceFunctions' class.
    """

    def test_dist_euclid(self):
        dist = DistanceFunctions.dist_euclid((3, 0))
        self.assertTrue(dist == 3)
        # You will want better tests than these ;)


if __name__ == '__main__':
    unittest.main()
