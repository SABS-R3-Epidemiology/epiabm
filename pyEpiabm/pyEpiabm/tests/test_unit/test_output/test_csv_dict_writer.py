import unittest
from unittest.mock import patch, mock_open, call, MagicMock
import os

import pyEpiabm as pe


class TestCsvDictWriter(unittest.TestCase):
    """Test the methods of the '_CsvDictWriter' class.
    """

    @patch('os.makedirs')
    def test_init(self, mock_mkdir):
        """Test the destructor method of the _CsvDictWriter class.
        """
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            mock_categories = ['Cat1', 'Cat2', 'Cat3']
            m = pe.output._CsvDictWriter('mock_folder', 'mock_filename',
                                         mock_categories)
            del m
        mo.assert_called_once_with(
            os.path.join('mock_folder', 'mock_filename'), 'w')
        mo().write.assert_called_once_with('Cat1,Cat2,Cat3\r\n')
        mock_mkdir.assert_called_with('mock_folder')

    @patch('os.makedirs')
    def test_write(self, mock_mkdir):
        """Test the write method of the _CsvDictWriter class.
        """
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            mock_categories = ['Cat1', 'Cat2', 'Cat3']
            new_content = {'Cat1': 'a', 'Cat3': 'c', 'Cat2': 'b'}
            m = pe.output._CsvDictWriter('mock_folder', 'mock_filename',
                                         mock_categories)
            m.write(new_content)
        mo().write.assert_has_calls([call('Cat1,Cat2,Cat3\r\n'),
                                    call('a,b,c\r\n')])

    @patch('os.makedirs')
    def test_del(self, mock_mkdir):
        """Test the destructor method of the _CsvDictWriter class.
        """
        fake_file = MagicMock()
        with patch("builtins.open", return_value=fake_file, create=True):
            mock_content = ['1', '2', '3']
            m = pe.output._CsvDictWriter('mock_folder', 'mock_filename',
                                         mock_content)
            m.__del__()
            fake_file.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
