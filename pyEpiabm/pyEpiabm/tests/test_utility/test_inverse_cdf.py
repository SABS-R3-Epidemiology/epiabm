import unittest
import numpy as np
from pyEpiabm.utility import InverseCdf


def test_construct(self):
    mean = 5
    icdf_array = np.ones(20)
    icdf_object = InverseCdf(mean, icdf_array)
    self.assertEqual(icdf_object.mean, 5)
    self.assertEqual(icdf_object.icdf_array, np.array([0.25, 0.50, 0.75]))


def test_choose_noexp(self):
    icdf_object = InverseCdf(3, np.ones(20))
    value = icdf_object.icdf_choose_noexp()
    self.assertTrue(0 <= value)


def test_choose_exp(self):
    icdf_object = InverseCdf(3, np.ones(20))
    value = icdf_object.icdf_choose_exp()
    self.assertTrue(0 <= value)


if __name__ == '__main__':
    unittest.main()
