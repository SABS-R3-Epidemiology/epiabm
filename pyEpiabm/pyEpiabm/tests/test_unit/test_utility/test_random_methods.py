import unittest

from pyEpiabm.utility import RandomMethods


class TestRandomMethods(unittest.TestCase):
    """Test the 'RandomMethods' class.
    """
    def test_init(self):
        """Tests that the class initialises with the correct
        random seed. The integers 163858 and 6573920043 were
        selected randomly for the 'RandomMethods' class.
        """
        r = RandomMethods()
        self.assertEqual(r.prev_s1, 163858)
        self.assertEqual(r.prev_s2, 6573920043)

    def test_covid_sim_rand(self):
        """Tests that the covid_sim_rand method returns the
        correct random numbers"""

        # Tests covid_sim_rand returns correct outputs
        """expected_outputs is a list of the first five outputs of the
        covid_sim_rand method when initialised with the seed s1=163858
        and s2=6573920043. As this seed won't be initialised with any
        other integers, the first 5 outputs should always be this list.
        """
        expected_outputs = [0.8716343138780989,
                            0.4994975046521462,
                            0.6333367446594049,
                            0.551876964936751,
                            0.8649655098663961]
        r = RandomMethods()
        outputs = []
        for _ in range(5):
            outputs.append(r.covid_sim_rand())

        self.assertAlmostEqual(outputs, expected_outputs)

        # Tests checks for negative s1, s2 in algorithm work

        # s1 and s2 values that give negative values that trigger the check
        r.prev_s1 = 10000000000
        r.prev_s2 = 10000000000

        # Set parameters and calculate expected s1 and s2 values
        Xm1 = 2147483563
        Xm2 = 2147483399
        Xa1 = 40014
        Xa2 = 40692
        k = r.prev_s1 // 53668
        expected_s1 = (Xa1 * (r.prev_s1 - k * 53668) - k * 12211) + Xm1
        k1 = r.prev_s2 // 52774
        expected_s2 = (Xa2 * (r.prev_s2 - k1 * 52774) - k1 * 3791) + Xm2

        # Calculate algorithm successfully adjusts the case of negative s1, s2
        r.covid_sim_rand()
        self.assertAlmostEqual(expected_s1, r.prev_s1)
        self.assertAlmostEqual(expected_s2, r.prev_s2)


if __name__ == '__main__':
    unittest.main()
