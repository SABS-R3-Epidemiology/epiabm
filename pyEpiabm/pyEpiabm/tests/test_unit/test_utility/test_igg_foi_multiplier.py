import unittest
from unittest import mock

from pyEpiabm.utility import IgGFOIMultiplier
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestIgGFOIMultiplier(TestPyEpiabm):
    """Test the 'RateMultiplier' class
    """

    def setUp(self):
        # This is the actual multiplier we will be using in simulations
        self.multiplier = IgGFOIMultiplier(4.26, 85.38, 0.21, 4.07, 24)

    def test_construct_erroneous(self):
        with self.assertRaises(ValueError) as ve_1:
            IgGFOIMultiplier(-1.0, 1.0, 0.1, 0.1, 1)
        self.assertEqual("max_41 must be positive", str(ve_1.exception))
        with self.assertRaises(ValueError) as ve_2:
            IgGFOIMultiplier(1.0, -1.0, 0.1, 0.1, 1)
        self.assertEqual("half_life_41 must be positive",
                         str(ve_2.exception))
        with self.assertRaises(ValueError) as ve_3:
            IgGFOIMultiplier(1.0, 1.0, 0.1, 0.1, -1)
        self.assertEqual("days_positive_pcr_to_max_igg must be positive",
                         str(ve_3.exception))
        with self.assertRaises(ValueError) as ve_4:
            IgGFOIMultiplier(1.0, 1.0, -0.3, 0.1, 1)
        self.assertEqual("change_in_max_10 is too large in magnitude "
                         "(4 * 0.3 > 1.0)",
                         str(ve_4.exception))
        with self.assertRaises(ValueError) as ve_5:
            IgGFOIMultiplier(1.0, 1.0, 0.1, 0.3, 1)
        self.assertEqual("change_in_half_life_10 is too large is too large "
                         "in magnitude (4 * 0.3 > 1.0)",
                         str(ve_5.exception))

    @mock.patch('pyEpiabm.utility.IgGFOIMultiplier._calculate_igg_titre')
    def test_construct(self, mock_calc):
        # Mock value for normalisation
        mock_calc.return_value = 4.0
        multiplier_1 = IgGFOIMultiplier(1.0, 2.0, 0.1, 0.2, 3)
        self.assertEqual(1.0, multiplier_1.max_41)
        self.assertEqual(2.0, multiplier_1.half_life_41)
        self.assertEqual(0.1, multiplier_1.change_in_max_10)
        self.assertEqual(0.2, multiplier_1.change_in_half_life_10)
        self.assertEqual(3, multiplier_1.days_positive_pcr_to_max_igg)
        self.assertEqual(4.0, multiplier_1.normalisation)

    def test__calculate_igg_titre(self):
        multiplier_1 = IgGFOIMultiplier(1.0, 2.0, 0.1, 0.2, 3)
        # Check the normalisation constant (from the construct method)
        self.assertEqual(1.4, multiplier_1.normalisation)

        time_since_max = 20.0
        age_group = 5
        titre = self.multiplier._calculate_igg_titre(time_since_max, age_group)
        self.assertAlmostEqual(3.312, titre, places=3)

    def test___call___before_max_igg(self):
        p = self.multiplier(20.0, 6)
        self.assertEqual(0, p)

    @mock.patch("pyEpiabm.Parameters.instance")
    def test___call___no_ages(self, mock_param):
        mock_param.return_value.use_ages = 0.0
        p = self.multiplier(104.0, 7)
        self.assertAlmostEqual(0.4777, p, places=4)

    def test___call___(self):
        p = self.multiplier(104.0, 7)
        self.assertAlmostEqual(0.5812, p, places=4)
        q = self.multiplier(26.0, 15)
        self.assertAlmostEqual(0.03412, q, places=5)


if __name__ == "__main__":
    unittest.main()
