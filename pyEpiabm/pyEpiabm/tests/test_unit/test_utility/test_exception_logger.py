import unittest
from unittest.mock import patch

from pyEpiabm.utility import log_exceptions


class ExampleClass:
    """Used to test the logger"""
    @log_exceptions()
    def sum_method(self, x, y):
        return x + y

    @log_exceptions(' - Fatal error in method')
    def annotated_method(self, x):
        x = 1/0
        return x


class TestDistanceFunctions(unittest.TestCase):
    """Test the 'DistanceFunctions' class.
    """
    @patch('logging.exception')
    def test_logger_no_return(self, mock_log):
        a = ExampleClass()
        a.sum_method(1, 'a')
        mock_log.assert_called_once_with("TypeError in"
                                         + " ExampleClass.sum_method()")

    def test_logger_return(self):
        """Ensure decorator allows value return"""
        a = ExampleClass()
        result = a.sum_method(1, 4)
        self.assertEqual(result, 5)

    @patch('logging.exception')
    def test_logger_annotated(self, mock_log):
        a = ExampleClass()
        a.annotated_method(1)
        mock_log.assert_called_once_with("ZeroDivisionError in"
                                         + " ExampleClass.annotated_method()"
                                         + " - Fatal error in method")


if __name__ == '__main__':
    unittest.main()
