import unittest
import numpy as np
from parameterized import parameterized

from pyEpiabm.utility import InverseCdf

numReps = 1


class TestInverseCdf(unittest.TestCase):
    """Test the 'InverseCDF' class.
    """
    def test_construct(self):
        mean = 5
        icdf_array = np.ones(20)
        icdf_object = InverseCdf(mean, icdf_array)
        self.assertEqual(icdf_object.mean, 5)
        self.assertEqual(icdf_object.icdf_array.all(), np.ones(20).all())

    @parameterized.expand([(np.random.rand(20) * numReps,)
                          for _ in range(numReps)])
    def test_choose_noexp(self, icdf):
        icdf = np.sort(icdf)
        icdf = 10 * icdf
        print(icdf)
        icdf_object = InverseCdf(3, icdf)
        value = icdf_object.icdf_choose_noexp()
        self.assertTrue(0 <= value)

    @parameterized.expand([(np.random.rand(20) * numReps,)
                           for _ in range(numReps)])
    def test_choose_exp(self, icdf):
        icdf = np.sort(icdf)
        icdf = 10 * icdf
        print(icdf)
        icdf_object = InverseCdf(3, icdf)
        value = icdf_object.icdf_choose_exp()
        self.assertTrue(0 <= value)


if __name__ == '__main__':
    unittest.main()
