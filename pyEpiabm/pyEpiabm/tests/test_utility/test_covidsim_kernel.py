import unittest
import numpy as np
from parameterized import parameterized

from pyEpiabm.utility.covidsim_kernel import SpatialKernel

numReps = 5


class TestSpatialKernel(unittest.TestCase):
    """Test the 'SpatialKernel' class.
    """
    @parameterized.expand([(np.random.rand(1) * numReps,)
                          for _ in range(numReps)])
    def test_kernel(self, dist):
        dist = 10 * dist[0]
        dist_object = SpatialKernel()
        value = dist_object.weighting(dist)
        self.assertTrue(0 <= value)

    @parameterized.expand([(np.random.rand(3) * numReps,)
                           for _ in range(numReps)])
    def test_kernel_shape_size(self, dist):
        dist = 10 * dist
        dist_object = SpatialKernel()
        value = dist_object.weighting(dist[0], dist[1], dist[2])
        self.assertTrue(0 <= value)

    def test_asserts(self):
        dist_object = SpatialKernel()
        example = dist_object.weighting(10, 10, 2)
        self.assertAlmostEqual(example, 0.25)
        example_small = dist_object.weighting(1, 10, 2)
        # Assert smaller distance has larger kernel
        self.assertTrue(example < example_small)
        self.assertRaises(AssertionError, dist_object.weighting, 10, -3, 2)
        self.assertRaises(AssertionError, dist_object.weighting, 10, 2, -2)


if __name__ == '__main__':
    unittest.main()
