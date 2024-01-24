import unittest
import numpy as np
from parameterized import parameterized

from pyEpiabm.utility import InverseCdf
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm

numReps = 1


class TestInverseCdf(TestPyEpiabm):
    """Test the 'InverseCDF' class.
    """
    def test_construct(self):
        mean = 5
        icdf_array = np.ones(21)
        icdf_object = InverseCdf(mean, icdf_array)
        self.assertEqual(icdf_object.mean, 5)
        self.assertEqual(icdf_object.icdf_array.all(), np.ones(21).all())

    @parameterized.expand([(np.random.rand(21) * numReps,)
                          for _ in range(numReps)])
    def test_choose_noexp(self, icdf):
        icdf = np.sort(icdf)
        icdf = 10 * icdf
        icdf_object = InverseCdf(3, icdf)
        value = icdf_object.icdf_choose_noexp()
        self.assertTrue(0 < value)

    @parameterized.expand([(np.random.rand(21) * numReps,)
                           for _ in range(numReps)])
    def test_choose_exp(self, icdf):
        icdf = np.sort(icdf)
        icdf = 10 * icdf
        icdf_object = InverseCdf(3, icdf)
        value = icdf_object.icdf_choose_exp()
        self.assertTrue(0 <= value)


if __name__ == '__main__':
    unittest.main()
