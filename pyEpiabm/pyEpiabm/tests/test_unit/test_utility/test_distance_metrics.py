import unittest
import numpy as np

import pyEpiabm as pe
from pyEpiabm.utility import DistanceFunctions
from pyEpiabm.tests.test_unit.mocked_logging_tests import TestMockedLogs


class TestDistanceFunctions(TestMockedLogs):
    """Test the 'DistanceFunctions' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super(TestDistanceFunctions, cls).setUpClass()
        # Sets up patch on logging

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

    def test_minimum_distance(self):
        f = DistanceFunctions.minimum_between_cells
        cell1 = pe.Cell()
        cell2 = pe.Cell((1, 1))
        for cell in [cell1, cell2]:
            cell.add_microcells(1)
        self.assertAlmostEqual(f(cell1, cell2), np.sqrt(2))
        cell2.microcells[0].set_location((1.0, 0.5))
        cell1.microcells[0].set_location((0.0, 0.5))
        self.assertAlmostEqual(f(cell1, cell2), 1)


if __name__ == '__main__':
    unittest.main()
