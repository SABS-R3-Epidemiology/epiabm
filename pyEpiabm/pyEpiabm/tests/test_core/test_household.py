import unittest

import pyEpiabm as pe


class TestHousehold(unittest.TestCase):
    """Test the 'Household' class.
    """
    def test_construct(self):
        pe.Household((1, 1))

    def test___repr__(self):
        subject = pe.Household((1, 1))
        self.assertIsInstance(repr(subject), str)
        test_string = "Household at (1.00, 1.00) with 0 people."
        self.assertEqual(repr(subject), test_string)

    def test_location_type(self):
        self.assertRaises(ValueError, pe.Household, (1, 1, 1))
        self.assertRaises(ValueError, pe.Household, (1, (8, 6)))
        self.assertRaises(ValueError, pe.Household, ([1, 1], 1))


if __name__ == '__main__':
    unittest.main()
