import unittest
import pyEpiabm as pe


class TestHousehold(unittest.TestCase):
    """
    Test the 'Household' class.
    """
    def test_construct(self):
        pe.Household((1, 1))

    def test___repr__(self):
        subject = pe.Household((1, 1))
        self.assertIsInstance(repr(subject), str)


if __name__ == '__main__':
    unittest.main()
