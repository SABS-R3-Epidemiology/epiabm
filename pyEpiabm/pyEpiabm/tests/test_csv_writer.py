import unittest
import pyEpiabm as pe
from unittest.mock import patch, mock_open
import os


class TestCsvWriter(unittest.TestCase):  # should it be Test_CsvWriter?
    """Test the '_CsvWriter' class.
    """

    def test_init(self):
        mo = mock_open()
        with patch('pyEpiabm._csv_writer.open', mo):
            mock_content = ['1', '2', '3']
            m = pe._CsvWriter('mock_filename', mock_content)
            del(m)
        #m.mock_calls
        #m.assert_called_once_with('mock_filename', mock_content)
        #m().write.assert_called_once_with(mock_content)
        print(mo().write.assert_called_once_with('1,2,3\r\n'))
        #content = mock_file.read()
        #print(content.__dict__)
        #self.assertEqual(content, '1, 2, 3')


if __name__ == '__main__':
    unittest.main()
