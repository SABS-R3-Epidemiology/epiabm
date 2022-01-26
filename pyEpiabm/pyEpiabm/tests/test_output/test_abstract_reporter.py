import unittest
from unittest import mock

import pyEpiabm as pe


class TestAbstractReporter(unittest.TestCase):
    """Test the 'AbstractReporter' class.
    """

    @mock.patch("os.path.exists", return_value=False)
    @mock.patch("os.makedirs")
    def test_construct(self, mock_makedir, mock_pathexists):
        reporter = pe.output.AbstractReporter("test_folder", False)
        self.assertEqual(reporter.folder, "test_folder")
        mock_pathexists.assert_called_once_with("test_folder")
        mock_makedir.assert_called_once_with("test_folder")

    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("os.scandir", return_value=[mock.MagicMock(),
                                            mock.MagicMock()])
    @mock.patch("os.remove")
    def test_construct_clearance(self, mock_remove, mock_scandir,
                                 mock_pathexists):
        pe.output.AbstractReporter("test_folder", True)
        mock_scandir.assert_called_once_with("test_folder")
        self.assertEqual(mock_remove.call_count, 2)  # For two elements in list

    @mock.patch("os.path.exists")
    @mock.patch("os.scandir", side_effect=IsADirectoryError)
    @mock.patch("os.remove")
    def test_construct_empty_clearance(self, mock_remove, mock_scandir,
                                       mock_pathexists):
        with self.assertRaises(IsADirectoryError):
            pe.output.AbstractReporter("test_folder", True)

    @mock.patch("os.path.exists")
    @mock.patch("os.makedirs")
    def test_write(self, mock_makedirs, mock_pathexists):
        mock.MagicMock(return_value=False)
        subject = pe.output.AbstractReporter("test_folder", False)
        self.assertRaises(NotImplementedError,
                          subject.write)


if __name__ == '__main__':
    unittest.main()
