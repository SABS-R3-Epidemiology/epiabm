import unittest
import pyEpiabm as pe


class TestParameters(unittest.TestCase):
    """Test the 'Parameters' class.
    """
    def test_instance(self):
        pe.core.Parameters.instance()

    def test_getattr(self):
        pe.core.Parameters.instance().aaa = 1
        self.assertEqual(pe.core.Parameters.instance().aaa, 1)

    def test_getattr_fails(self):
        with self.assertRaises(AttributeError):
            pe.core.Parameters.instance().bbb


if __name__ == '__main__':
    unittest.main()
