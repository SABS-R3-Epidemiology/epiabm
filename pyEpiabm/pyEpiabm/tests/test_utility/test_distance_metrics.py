import unittest

from pyEpiabm.utility import DistanceFunctions


class TestDistanceFunctions(unittest.TestCase):
    """Test the 'DistanceFunctions' class.
    """

    def test_dist_euclid(self):
        dist = DistanceFunctions.dist_euclid((3, 0))
        self.assertTrue(dist == 3)

        dist = DistanceFunctions.dist_euclid((-3, 0))
        self.assertTrue(dist == 3)

        dist = DistanceFunctions.dist_euclid((-3, 0), (3, 0))
        self.assertTrue(dist == 6)

        dist = DistanceFunctions.dist_euclid((-2, 0), (1, 4))
        self.assertTrue(dist == 5.0)

    def test_dist(self):
        f = DistanceFunctions.dist
        self.assertAlmostEqual(f((3, 0)), 3)
        self.assertAlmostEqual(f((-3, 0)), 3)
        self.assertAlmostEqual(f((-3, 0), (3, 0)), 6)
        self.assertAlmostEqual(f((-2, 0), (1, 4)), 5)
    
    def test_periodic(self):
        f = DistanceFunctions.dist_periodic
        stride = (5, 4)
        scales = (10, 8)

        self.assertAlmostEqual(f((2, 0), stride, scales), 4)
        self.assertAlmostEqual(f((-3, 0), stride, scales), 4)
        self.assertAlmostEqual(f((-3, 0), stride, scales, (3, 0)), 2)
        self.assertAlmostEqual(f((1, -3), stride, scales, (1, 4)), 4)


if __name__ == '__main__':
    unittest.main()
