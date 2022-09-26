import unittest
from unittest.mock import patch, mock_open, call, MagicMock
import random
import os

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestNewCasesWriter(TestPyEpiabm):
    """Test the methods of the '_CsvWriter' class.
    """

    @patch('os.makedirs')
    def test_init(self, mock_mkdir):
        """Test the constructor method of the NewCasesWriter class.
        """
        mo = mock_open()
        with patch('pyEpiabm.output._csv_writer.open', mo):
            m = pe.output.NewCasesWriter('mock_folder')
            del m
        mo.assert_called_once_with(
            os.path.join('mock_folder', 'new_cases.csv'), 'w')
        mo().write.assert_called_once_with('t,cell,new_cases\r\n')
        mock_mkdir.assert_called_with('mock_folder')

    @patch('os.makedirs')
    def test_write(self, mock_mkdir):
        """Test the write method of the NewCasesWriter class.
        """
        n_susc = random.randint(5, 100)
        n_old_cases = random.randint(10, 100)
        n_new_cases = random.randint(1, 20)
        mo = mock_open()
        pe.Parameters.instance().time_steps_per_day = 1
        p = pe.Population()
        p.cells = [pe.Cell()]
        p.cells[0].microcells = [pe.Microcell(p.cells[0])]
        p.cells[0].persons = [
            pe.Person(p.cells[0].microcells[0]) for i in range(
                n_susc + n_old_cases + n_new_cases)]
        for i in range(n_old_cases):
            p.cells[0].persons[i].infection_start_time = 1.0
        for i in range(n_old_cases, n_old_cases + n_new_cases):
            p.cells[0].persons[i].infection_start_time = 10.0

        with patch('pyEpiabm.output._csv_writer.open', mo):
            m = pe.output.NewCasesWriter('mock_folder')
            m.write(10, p)
        mo().write.assert_has_calls([
            call('t,cell,new_cases\r\n'),
            call(f'10,{p.cells[0].id},{n_new_cases}\r\n')])

    @patch('os.makedirs')
    def test_del(self, mock_mkdir):
        """Test the destructor method of the NewCasesWriter class.
        """
        fake_file = MagicMock()
        with patch("builtins.open", return_value=fake_file, create=True):
            m = pe.output.NewCasesWriter('mock_folder')
            m.__del__()
            fake_file.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
