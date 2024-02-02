import unittest
from unittest import mock

from pyEpiabm.utility import RateMultiplier
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestRateMultiplier(TestPyEpiabm):
    """Test the 'RateMultiplier' class
    """
    def test_construct_erroneous(self):
        with self.assertRaises(ValueError) as ve_1:
            RateMultiplier(p_1=0.5, p_2=0.6, t_1=-1.0, t_2=2.0)
        self.assertEqual("t_1 must be smaller than t_2 and both must"
                         "be non-negative", str(ve_1.exception))
        with self.assertRaises(ValueError) as ve_2:
            RateMultiplier(p_1=0.5, p_2=0.6, t_1=3.0, t_2=2.0)
        self.assertEqual("t_1 must be smaller than t_2 and both must"
                         "be non-negative", str(ve_2.exception))
        with self.assertRaises(ValueError) as ve_3:
            RateMultiplier(p_1=0.5, p_2=0.4, t_1=0.0, t_2=2.0)
        self.assertEqual("p_1 must be smaller than p_2 and both must"
                         "lie between 0 and 1 inclusive", str(ve_3.exception))
        with self.assertRaises(ValueError) as ve_4:
            RateMultiplier(p_1=-0.5, p_2=0.6, t_1=0.0, t_2=2.0)
        self.assertEqual("p_1 must be smaller than p_2 and both must"
                         "lie between 0 and 1 inclusive", str(ve_4.exception))
        with self.assertRaises(ValueError) as ve_5:
            RateMultiplier(p_1=0.5, p_2=1.6, t_1=0.0, t_2=2.0)
        self.assertEqual("p_1 must be smaller than p_2 and both must"
                         "lie between 0 and 1 inclusive", str(ve_5.exception))

    @mock.patch('pyEpiabm.utility.RateMultiplier._calculate_parameters')
    def test_construct(self, mock_calc):
        # Mock values for a and b
        mock_calc.return_value = 1.0, 2.0
        multiplier_1 = RateMultiplier(p_1=0.5, p_2=1.0, t_1=0.0, t_2=1.0)
        self.assertEqual(0.5, multiplier_1.p_1)
        self.assertEqual(1.0, multiplier_1.p_2)
        self.assertEqual(0.0, multiplier_1.t_1)
        self.assertEqual(1.0, multiplier_1.t_2)
        self.assertEqual(1.0, multiplier_1.a)
        self.assertEqual(2.0, multiplier_1.b)
        # Test defaults
        multiplier_2 = RateMultiplier(p_1=0.5, p_2=0.6)
        self.assertEqual(90.0, multiplier_2.t_1)
        self.assertEqual(180.0, multiplier_2.t_2)

    def test__calculate_parameters(self):
        multiplier_1 = RateMultiplier(p_1=0.5, p_2=1.0, t_1=0.0, t_2=1.0)
        self.assertEqual(0.0, multiplier_1.a)
        self.assertEqual(0.0, multiplier_1.b)

        # Below uses real data point values
        multiplier_2 = RateMultiplier(p_1=0.750, p_2=0.842,
                                      t_1=90.0, t_2=180.0)
        self.assertAlmostEqual(0.00510, multiplier_2.a, places=5)
        self.assertAlmostEqual(0.396, multiplier_2.b, places=3)

    def test___call___erroneous(self):
        multiplier = RateMultiplier(p_1=0.5, p_2=0.6)
        with self.assertRaises(ValueError) as ve:
            multiplier(-1.0)
        self.assertEqual("t must be non-negative", str(ve.exception))

    def test___call__(self):
        multiplier_1 = RateMultiplier(p_1=0.5, p_2=1.0, t_1=0.0, t_2=1.0)
        self.assertEqual(1.0, multiplier_1(5.0))

        # This gives a value of b greater than 1, with log(b)/a = 78.307...
        multiplier_2 = RateMultiplier(p_1=0.1, p_2=0.6)
        self.assertEqual(0.0, multiplier_2(45.0))
        self.assertEqual(0.0, multiplier_2(78.3))
        self.assertAlmostEqual(0.1, multiplier_2(90.0))
        self.assertAlmostEqual(0.6, multiplier_2(180.0))
        self.assertAlmostEqual(0.4, multiplier_2(135.0))
        self.assertAlmostEqual(0.92099, multiplier_2(360.0), places=5)

if __name__ == "__main__":
    unittest.main()
