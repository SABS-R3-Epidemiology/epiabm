import unittest

from pyEpiabm.utility import RandomMethods


class TestInfectionStatus(unittest.TestCase):
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

    def test_random_number(self):
        """Tests that the random_number method returns the
        a valid integer.
        """
        number = RandomMethods.random_number()
        self.assertTrue(number >= 0)

    def test_covid_sim_rand(self):
        """Tests that the covid_sim_rand method returns the
        correct random numbers"""

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


if __name__ == '__main__':
    unittest.main()
