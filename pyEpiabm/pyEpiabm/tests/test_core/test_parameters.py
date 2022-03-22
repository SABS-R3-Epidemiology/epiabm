from collections import defaultdict
import unittest
from unittest.mock import patch
import os

import pyEpiabm as pe
from pyEpiabm.tests.parameter_config_tests import TestPyEpiabm


class TestParameters(TestPyEpiabm):
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
        my_dict = defaultdict(int, my_dict)
        self.assertEqual(my_dict["false_key"], 0)


class TestNoConfigParameters(unittest.TestCase):
    """Test class for tests without implicit config call
    in the test class setUp.
    """
    def tearDown(self):
        if pe.Parameters._instance:
            pe.Parameters._instance = None

    def test_runtime_error(self):
        with self.assertRaises(RuntimeError):
            pe.Parameters.instance()

    @patch('json.loads')
    @patch('builtins.open')
    def test_set_file(self, mock_open, mock_load):
        param_loc = ("pyEpiabm/pyEpiabm/tests/"
                     + "testing_parameters.json")
        mock_load.return_value = {}
        pe.Parameters.set_file(param_loc)
        mock_load.assert_called_once()
        mock_open.assert_called_once_with(param_loc, 'r')

    @patch('json.loads')
    def test_read_numbers(self, mock_load):
        param_loc = os.path.join(os.path.dirname(__file__),
                                 os.pardir, 'testing_parameters.json')
        mock_load.return_value = {
            'val1': 1,
            'val2': 2.0}

        pe.Parameters.set_file(param_loc)
        mock_load.assert_called_once()
        self.assertEqual(pe.Parameters.instance().val1, 1)
        self.assertEqual(pe.Parameters.instance().val2, 2.0)

    @patch('json.loads')
    def test_read_lists(self, mock_load):
        param_loc = os.path.join(os.path.dirname(__file__),
                                 os.pardir, 'testing_parameters.json')
        list_val = [0, 0.33, 0.66, 1]
        mock_load.return_value = {
            'list1': list_val}

        pe.Parameters.set_file(param_loc)
        mock_load.assert_called_once()
        self.assertListEqual(list(pe.Parameters.instance().list1), list_val)


if __name__ == '__main__':
    unittest.main()
