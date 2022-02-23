import unittest
from unittest.mock import patch, mock_open, call, MagicMock

import pyEpiabm as pe


class TestCsvWriter(unittest.TestCase):
    """Test the methods of the '_CsvWriter' class.
    """

    @patch('os.makedirs')
    def test_init(self, mock_mkdir):
        """Test the constructor method of the _CsvWriter class.
        """
        mo = mock_open()
        with patch('pyEpiabm.output._csv_writer.open', mo):
            mock_content = ['1', '2', '3']
            m = pe.output._CsvWriter('mock_folder', 'mock_filename',
                                     mock_content)
            del(m)
        mo.assert_called_once_with('mock_filename', 'w')
        mo().write.assert_called_once_with('1,2,3\r\n')
        mock_mkdir.assert_called_with('mock_folder')

    @patch('os.makedirs')
    def test_write(self, mock_mkdir):
        """Test the write method of the _CsvWriter class.
        """
        mo = mock_open()
        with patch('pyEpiabm.output._csv_writer.open', mo):
            mock_content = ['1', '2', '3']
            new_content = ['a', 'b', 'c']
            m = pe.output._CsvWriter('mock_folder', 'mock_filename',
                                     mock_content)
            m.write(new_content)
        mo().write.assert_has_calls([call('1,2,3\r\n'), call('a,b,c\r\n')])

    @patch('os.makedirs')
    def test_del(self, mock_mkdir):
        """Test the destructor method of the _CsvWriter class.
        """
        fake_file = MagicMock()
        with patch("builtins.open", return_value=fake_file, create=True):
            mock_content = ['1', '2', '3']
            m = pe.output._CsvWriter('mock_folder', 'mock_filename',
                                     mock_content)
            m.__del__()
            fake_file.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
