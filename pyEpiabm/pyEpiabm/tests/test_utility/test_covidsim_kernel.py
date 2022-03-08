import unittest
import numpy as np
from parameterized import parameterized

from pyEpiabm.utility import Kernel

numReps = 1


class TestKernel(unittest.TestCase):
    """Test the 'Kernel' class.
    """
    @parameterized.expand([(np.random.rand(1) * numReps,)
                          for _ in range(numReps)])
    def test_kernel(self, dist):
        dist = np.sort(dist)
        dist = 10 * dist[0]
        dist_object = Kernel()
        value = dist_object.weighting(dist)
        print(value)
        self.assertTrue(0 <= value)

    @parameterized.expand([(np.random.rand(3) * numReps,)
                           for _ in range(numReps)])
    def test_kernel_shape_size(self, dist):
        dist = np.sort(dist)
        dist = 10 * dist
        dist_object = Kernel()
        value = dist_object.weighting(dist[0], dist[1], dist[2])
        self.assertTrue(0 <= value)


if __name__ == '__main__':
    unittest.main()
