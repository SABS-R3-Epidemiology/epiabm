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

    def test_default_dict(self):
        my_dict = pe.Parameters.instance().host_progression_lists
        self.assertIsInstance(my_dict["prob_gp_to_hosp"], list)
        self.assertEqual(my_dict["false_key"], 0)


if __name__ == '__main__':
    unittest.main()
