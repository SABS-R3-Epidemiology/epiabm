import unittest
import pyEpiabm as pe


class TestCovidsimHelpers(unittest.TestCase):
    """Test the 'CovidsimHelpers' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)
        cls.infector = pe.Person(cls.microcell)
        cls.infectee = pe.Person(cls.microcell)

    def test_calc_house_inf(self):
        value = pe.CovidsimHelpers.calc_house_inf(self.infector, 0)
        self.assertEqual(value, 1.0)  # Will have to update with function
        self.assertIsInstance(value, float)

    def test_calc_house_susc(self):
        value_house = pe.CovidsimHelpers.calc_house_susc(self.infector,
                                                         self.infectee, 0)
        value_person = pe.CovidsimHelpers.calc_person_susc(self.infector,
                                                           self.infectee, 0)
        self.assertEqual(value_house, value_person)  # Update with function
        self.assertIsInstance(value_house, float)

    def test_calc_person_susc(self):
        value_2 = pe.CovidsimHelpers.calc_person_susc(self.infector,
                                                      self.infectee, 0)
        self.assertEqual(value_2, 1.0)  # Will have to update with function
        self.assertIsInstance(value_2, float)


if __name__ == '__main__':
    unittest.main()
