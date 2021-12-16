import unittest
import pyEpiabm as pe
from unittest.mock import patch, mock_open, call, MagicMock


class TestCsvWriter(unittest.TestCase):
    """Test the three methods of the '_CsvWriter' class.
    """

    def test_init(self):
        """Test the __init__ method of the _CsvWriter class.
        """
        mo = mock_open()
        with patch('pyEpiabm._csv_writer.open', mo):
            mock_content = ['1', '2', '3']
            m = pe._CsvWriter('mock_filename', mock_content)
            del(m)
        mo.assert_called_once_with('mock_filename', 'w')
        mo().write.assert_called_once_with('1,2,3\r\n')

    def test_file_not_found(self):
        mock_content = ['1', '2', '3']
        with self.assertRaises(FileNotFoundError):
            test_writer = pe._CsvWriter('mocked_folder/test_file',
                                        mock_content)
            self.assertIsNone(test_writer.f)
            self.assertIsNone(test_writer.writer)
        self.assertRaises(FileNotFoundError, pe._CsvWriter,
                          'mocked_folder/test_file', mock_content)

    def test_write(self):
        """Test the write method of the _CsvWriter class.
        """
        mo = mock_open()
        with patch('pyEpiabm._csv_writer.open', mo):
            mock_content = ['1', '2', '3']
            new_content = ['a', 'b', 'c']
            m = pe._CsvWriter('mock_filename', mock_content)
            m.write(new_content)
        mo().write.assert_has_calls([call('1,2,3\r\n'), call('a,b,c\r\n')])

    def test_del(self):
        """Test the __del__ method of the _CsvWriter class.
        """
        fake_file = MagicMock()
        with patch("builtins.open", return_value=fake_file, create=True):
            mock_content = ['1', '2', '3']
            m = pe._CsvWriter('mock_filename', mock_content)
            m.__del__()
            fake_file.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
