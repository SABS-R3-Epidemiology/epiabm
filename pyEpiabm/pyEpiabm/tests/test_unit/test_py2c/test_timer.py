import re
import unittest
from unittest import mock

from pyEpiabm.py2c.py2c_population import _Timer
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestTimer(TestPyEpiabm):
    """Test the 'Timer' class.
    """

    @mock.patch('builtins.print')
    def test__init__(self, _):
        named_timer = _Timer('my_name')
        self.assertEqual(named_timer.name, 'my_name')

    @mock.patch('builtins.print')
    def test__del__(self, mock_print):
        timer = _Timer('timer')
        del timer
        mock_print.assert_called_once()
        re_scientific_notation = r"(?:0|[1-9]\d*)(?:\.\d+)?(?:[e][+\-]?\d+)?"
        self.assertTrue(re.fullmatch(f"timer took {re_scientific_notation}s",
                                     mock_print.call_args.args[0]))


if __name__ == '__main__':
    unittest.main()
