import unittest
from unittest.mock import patch
import pandas as pd
from packaging import version

import pyEpiabm as pe
from pyEpiabm.core import Population
from pyEpiabm.routine import FilePopulationFactory
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestPopConfig(TestPyEpiabm):
    """Test the 'ToyPopConfig' class.
    """

    def setUp(self) -> None:
        self.input = {'cell': [1.0, 2.0], 'microcell': [1.0, 1.0],
                      'location_x': [0.0, 1.0], 'location_y': [0.0, 1.0],
                      'household_number': [1, 1],
                      'Susceptible': [8, 9], 'InfectMild': [2, 3]}
        self.df = pd.DataFrame(self.input)

    @patch('logging.exception')
    def test_make_pop_no_file(self, mock_log):
        """Tests for when no file is specified.
        """
        FilePopulationFactory.make_pop()
        mock_log.assert_called_once_with("TypeError in"
                                         + " FilePopulationFactory.make_pop()")

    @patch("pandas.read_csv")
    def test_make_pop(self, mock_read):
        """Tests for when the population is read in from file.
        """
        # Population is initialised with no households
        mock_read.return_value = self.df

        test_pop = FilePopulationFactory.make_pop('test_input.csv')
        mock_read.assert_called_once_with('test_input.csv')

        total_people = 0
        total_infectious = 0
        count_non_empty_cells = 0
        for cell in test_pop.cells:
            total_infectious += cell.number_infectious()
            for microcell in cell.microcells:
                total_people += len(microcell.persons)
            if len(cell.persons) > 0:
                count_non_empty_cells += 1

        # Test there are at least one non-empty cell
        self.assertTrue(count_non_empty_cells == 2)

        # Test that everyone in the population has been assigned a microcell
        self.assertEqual(total_people, 22)

        # Test a population class object is returned
        self.assertIsInstance(test_pop, pe.Population)

    @patch('logging.exception')
    @patch("pandas.read_csv")
    def test_make_pop_exception(self, mock_read, mock_log):
        """Tests for when the population is read from empty file.
        """
        mock_read.side_effect = FileNotFoundError

        FilePopulationFactory.make_pop('test_input.csv')
        mock_log.assert_called_once_with("FileNotFoundError in"
                                         + " FilePopulationFactory.make_pop()")

    @patch('logging.exception')
    @patch("pandas.read_csv")
    def test_invalid_input(self, mock_read, mock_log):
        """Test error handling for unknown column name
        """
        # Read in data with incorrect infection status
        data = self.df.rename(columns={'InfectMild': 'InfectUnknown'})
        mock_read.return_value = data

        FilePopulationFactory.make_pop('test_input.csv')
        mock_log.assert_called_once_with("ValueError in FilePopulation"
                                         + "Factory.make_pop()")
        mock_read.assert_called_once_with('test_input.csv')

    @patch('logging.exception')
    @patch("pandas.read_csv")
    def test_duplicate_microcell(self, mock_read, mock_log):
        """Test error handling for duplicate microcell
        """
        # Move second microcell to first cell (with duplicate id)

        self.df.iat[1, 0] = 1

        mock_read.return_value = self.df

        FilePopulationFactory.make_pop('test_input.csv')
        mock_log.assert_called_once_with("ValueError in FilePopulation"
                                         + "Factory.make_pop()")
        mock_read.assert_called_once_with('test_input.csv')

    def test_find_cell(self):
        pop = pe.Population()
        pop.add_cells(2)
        pop.cells[1].set_id(42)

        target_cell = FilePopulationFactory.find_cell(pop, 42)
        self.assertEqual(target_cell.id, 42)
        self.assertEqual(hash(target_cell), hash(pop.cells[1]))
        self.assertEqual(len(pop.cells), 2)  # No new cell created

        new_cell = FilePopulationFactory.find_cell(pop, 43)
        self.assertEqual(new_cell.id, 43)
        self.assertEqual(len(pop.cells), 3)  # New cell created

    @patch("pandas.read_csv")
    def test_add_households(self, mock_read):
        """Tests when households are implemented.
        """
        # Define multiple households in cells
        self.df['household_number'] = pd.Series([2, 3])
        mock_read.return_value = self.df

        test_pop = FilePopulationFactory.make_pop('test_input.csv')

        total_people = 0
        households = []
        num_empty_households = 0
        for cell in test_pop.cells:
            for microcell in cell.microcells:
                for person in microcell.persons:
                    if person.household not in households:
                        households.append(person.household)
                    if len(person.household.persons) == 0:
                        num_empty_households += 1
                    total_people += len(person.household.persons)

        # Some households may be empty so won't be included
        self.assertTrue(len(households) <= 5)
        self.assertTrue(num_empty_households < 5)

    def summarise_households(self, pop: Population):
        # Returns lists of cell and microcell wise populations
        # Not a testing function, but used in test below

        households = []
        sizes = []
        for cell in pop.cells:
            for microcell in cell.microcells:
                for person in microcell.persons:
                    if person.household not in households:
                        households.append(person.household)
                        sizes.append(len(person.household.persons))
        return sizes

    @patch("pandas.read_csv")
    def test_household_seed(self, mock_read):
        """Tests household allocation is consistent with random seed
        """
        input = {'cell': [1, 2], 'microcell': [1, 1],
                 'household_number': [10, 10],
                 'Susceptible': [200, 200]}
        df = pd.DataFrame(input)
        mock_read.return_value = df

        # Create two identical populations with the same seed
        seed_pop = FilePopulationFactory.make_pop('mock_file', 42)
        comp_pop = FilePopulationFactory.make_pop('mock_file', 42)

        self.assertEqual(str(seed_pop), str(comp_pop))

        seed_households = self.summarise_households(seed_pop)
        comp_households = self.summarise_households(comp_pop)
        self.assertEqual(seed_households, comp_households)

        # Also compare to a population with a different seed
        diff_pop = FilePopulationFactory().make_pop('mock_file', 43)

        diff_households = self.summarise_households(diff_pop)
        self.assertNotEqual(seed_households, diff_households)

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_print_population_loc(self, mock_write, mock_read):
        """Tests method to print population to csv, to ensure that
        the file outputs to the correct location.
        """
        mock_read.return_value = self.df

        test_pop = FilePopulationFactory.make_pop('test_input.csv')
        self.assertEqual(len(test_pop.cells), 2)
        self.assertEqual(test_pop.total_people(), 22)

        FilePopulationFactory.print_population(test_pop, 'output.csv')
        mock_write.assert_called_once()
        self.assertEqual(mock_write.call_args[0], ('output.csv',))

    @patch("pandas.read_csv")
    @patch("copy.copy")
    def test_print_population(self, mock_copy, mock_read):
        """Tests method to print population to csv, to match content
        with target. Uses meaningful household data.
        """
        self.df['household_number'] = pd.Series([2, 3])
        mock_read.return_value = self.df

        test_pop = FilePopulationFactory.make_pop('test_input.csv')
        self.assertEqual(len(test_pop.cells), 2)
        self.assertEqual(test_pop.total_people(), 22)

        FilePopulationFactory.print_population(test_pop, 'output.csv')
        if version.parse(pd.__version__) >= version.parse("1.4.0"):
            pd.testing.assert_frame_equal(mock_copy.call_args.args[0],
                                          self.df, check_dtype=False)

    @patch('logging.exception')
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_print_pop_exception(self, mock_read, mock_print, mock_log):
        """Tests for when the population is read from empty file.
        """
        mock_print.side_effect = FileNotFoundError
        mock_read.return_value = self.df

        test_pop = FilePopulationFactory.make_pop('test_input.csv')

        FilePopulationFactory.print_population(test_pop, 'output.csv')

        mock_log.assert_called_once_with("FileNotFoundError in FilePopulation"
                                         + "Factory.print_population()")

    @patch("pandas.read_csv")
    @patch("copy.copy")
    @patch("logging.warning")
    @patch.object(pd, '__version__', "1.3.0")
    def test_print_population_dependancy(self, mock_logger,
                                         mock_copy, mock_read):
        """Tests method to print population to csv, to match content
        with target.
        """
        test_pop = FilePopulationFactory.make_pop('test_input.csv')

        FilePopulationFactory.print_population(test_pop, 'output.csv')
        mock_logger.assert_called_once()


if __name__ == '__main__':
    unittest.main()
