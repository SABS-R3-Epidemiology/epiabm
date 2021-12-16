import unittest
import pyEpiabm as pe
from unittest.mock import patch, mock_open, call


class TestCsvWriter(unittest.TestCase):  # should it be Test_CsvWriter?
    """Test the '_CsvWriter' class.
    """

    def test_init(self):
        mo = mock_open()
        with patch('pyEpiabm._csv_writer.open', mo):
            mock_content = ['1', '2', '3']
            m = pe._CsvWriter('mock_filename', mock_content)
            del(m)
        mo.assert_called_once_with('mock_filename', 'w')
        mo().write.assert_called_once_with('1,2,3\r\n')

    def test_write(self):
        # Set up of the file
        mo = mock_open()
        with patch('pyEpiabm._csv_writer.open', mo):
            mock_content = ['1', '2', '3']
            new_content = ['a', 'b', 'c']
            m = pe._CsvWriter('mock_filename', mock_content)
            m.write(new_content)
        # Test to add a row
        mo().write.assert_has_calls([call('1,2,3\r\n'), call('a,b,c\r\n')])


if __name__ == '__main__':
    unittest.main()
