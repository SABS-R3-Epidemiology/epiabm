import unittest

import pyEpiabm as pe


class TestParameters(unittest.TestCase):
    """Test the 'Parameters' class.
    """
    def test_instance(self):
        pe.Parameters.instance()

    def test_getattr(self):
        pe.Parameters.instance().aaa = 1
        self.assertEqual(pe.Parameters.instance().aaa, 1)

    def test_getattr_fails(self):
        with self.assertRaises(AttributeError):
            pe.Parameters.instance().bbb


if __name__ == '__main__':
    unittest.main()
