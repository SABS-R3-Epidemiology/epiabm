import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.py2c.py2c_population import _py2c_converter
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestPy2C_Convertor(TestPyEpiabm):
    """Test the 'py2c_convertor' class.
    """
    @classmethod
    def setUp(self) -> None:
        """Sets up a population we can use throughout the test.
        2 people are located in one microcell.
        """
        # Set up population for conversion to cEpiabm
        self.pop = pe.Population()
        self.pop.add_cells(1)
        self.cell = self.pop.cells[0]
        self.cell.add_microcells(1)
        self.microcell = self.cell.microcells[0]
        self.microcell.add_people(2)
        self.persons = self.pop.cells[0].microcells[0].persons

        # Add location complexity to population
        self.house = pe.Household(self.microcell, [1.0, 1.0])
        self.house.persons = [self.persons[0]]
        self.persons[0].household = self.house

        self.microcell.add_place(1, (1, 1),  pe.property.PlaceType.Workplace)
        self.microcell.places[0].add_person(self.persons[0])

        # Create mock cEpiabm objects for use in conversion call
        self.cpp_fac = mock.Mock()
        self.cpp_map = mock.MagicMock()
        self.cpp_map.__getitem__.side_effect = lambda x: getattr(self.cpp_map,
                                                                 str(x))

    converter_path = 'pyEpiabm.py2c.py2c_population._py2c_converter'

    @mock.patch(converter_path)
    def test_converter_func(self, mock_converter):
        mock_converter.side_effect = NotImplementedError()
        with self.assertRaises(NotImplementedError):
            pe.py2c.py2c_convert_population(self.pop, self.cpp_fac,
                                            self.cpp_map)
            mock_converter.assert_called_once_with(self.pop, self.cpp_fac,
                                                   self.cpp_map)

    @mock.patch(converter_path + '._link_places')
    @mock.patch(converter_path + '._configure_households')
    @mock.patch(converter_path + '._configure_people')
    @mock.patch(converter_path + '._add_people')
    @mock.patch(converter_path + '._copy_structure')
    @mock.patch('builtins.print')
    def test__init__(self, _,  *converter_mocks):
        converter = _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)
        self.assertEqual(converter.py_population, self.pop)
        self.assertEqual(converter.c_factory, self.cpp_fac)
        self.assertEqual(converter.c_population, None)
        self.assertEqual(converter.c_status_map, self.cpp_map)
        for converter_mock in converter_mocks:
            converter_mock.assert_called_once_with()

    @mock.patch(converter_path + '._validate_households')
    @mock.patch('builtins.print')
    def test_index_population(self, mock_print, mock_validate):
        mock_validate.side_effect = NotImplementedError()
        with self.assertRaises(NotImplementedError):
            # This stops initialisation after index_pop call
            converter = _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)
            self.assertEqual(converter.households, self.house)
            self.assertEqual(converter.n_places, 1)

        self.assertIn('_index_population took',
                      mock_print.call_args_list[-1][0][0])

    @mock.patch(converter_path + '._copy_structure')
    @mock.patch('builtins.print')
    def test_validate_households(self, mock_print, mock_copy):
        mock_copy.side_effect = NotImplementedError()
        with self.assertRaises(NotImplementedError):
            converter = _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)
            self.assertEqual(converter.households, self.house)

            self.house._microcell_index = None
            self.house.persons = []  # Artifical empty household
            converter = _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)

        self.assertIn('_validate_households took',
                      mock_print.call_args_list[-1][0][0])

    @mock.patch(converter_path + '._link_places')
    @mock.patch(converter_path + '._configure_households')
    @mock.patch(converter_path + '._configure_people')
    @mock.patch(converter_path + '._add_people')
    @mock.patch(converter_path + '._copy_structure')
    @mock.patch('builtins.print')
    def test_catch_misindexed_households(self, _, *convertor_mocks):
        # Run converter to generate correct household list
        converter = _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)

        # Modify household set to add error
        temp_house = converter.households.pop()
        temp_house._microcell_index = 2
        converter.households.add(temp_house)

        with self.assertRaises(AssertionError) as context:
            converter._validate_households()

        err_msg = "Household cannot link two people in different microcells."
        self.assertEqual(context.exception.args[0], err_msg)

    @mock.patch(converter_path + '._link_places')
    @mock.patch(converter_path + '._configure_households')
    @mock.patch(converter_path + '._configure_people')
    @mock.patch(converter_path + '._add_people')
    @mock.patch(converter_path + '._copy_structure')
    @mock.patch('builtins.print')
    def test_catch_empty_households(self, mock_print, *convertor_mocks):
        # Run converter to generate correct household list
        converter = _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)

        # Modify household set to add error
        temp_house = converter.households.pop()
        temp_house.persons = []
        temp_house._microcell_index = None
        converter.households.add(temp_house)
        converter._validate_households()

        # Check penultimate print call (before second validation timing)
        err_msg = "Warning: Empty Household exists."
        self.assertEqual(str(mock_print.call_args_list[-2][0][0]), err_msg)

    def generate_cpp_mocked_pop(self):
        cpp_mcell, cpp_cell, cpp_pop = [mock.Mock()] * 3
        cpp_cell.microcells.return_value = [cpp_mcell]
        cpp_pop.cells.return_value = [cpp_cell]

        cpp_cell.index.return_value = 0
        cpp_cell.get_microcell.return_value = cpp_mcell
        cpp_pop.get_cell.return_value = cpp_cell
        return cpp_mcell, cpp_cell, cpp_pop

    @mock.patch(converter_path + '._add_people')
    @mock.patch('builtins.print')
    def test_copy_structure(self, mock_print, mock_add):
        mock_add.side_effect = NotImplementedError()
        cpp_mcell, cpp_cell, cpp_pop = self.generate_cpp_mocked_pop()
        self.cpp_fac.make_empty_population.return_value = cpp_pop

        with self.assertRaises(NotImplementedError):
            _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)
        self.cpp_fac.add_microcells.assert_called_once_with(cpp_cell, 1)
        self.cpp_fac.add_households.assert_called_once_with(cpp_mcell, 1)

        self.assertIn('_copy_structure took',
                      mock_print.call_args_list[-1][0][0])

    @mock.patch(converter_path + '._configure_people')
    @mock.patch('builtins.print')
    def test_add_people(self, mock_print, mock_conf):
        mock_conf.side_effect = NotImplementedError()
        cpp_mcell, cpp_cell, cpp_pop = self.generate_cpp_mocked_pop()
        self.cpp_fac.make_empty_population.return_value = cpp_pop

        with self.assertRaises(NotImplementedError):
            _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)
        cpp_pop.get_cell.assert_called_once_with(0)
        cpp_cell.get_microcell.assert_called_once_with(0)
        self.cpp_fac.add_persons.assert_called_once_with(cpp_cell,
                                                         cpp_mcell, 2)

        self.assertIn('_add_people took',
                      mock_print.call_args_list[-1][0][0])

    @mock.patch(converter_path + '._configure_households')
    @mock.patch('builtins.print')
    def test_configure_people(self, mock_print, mock_conf):
        mock_conf.side_effect = NotImplementedError()
        _, cpp_cell, cpp_pop = self.generate_cpp_mocked_pop()

        cpp_person = mock.Mock()
        cpp_params = mock.MagicMock()
        cpp_person.params.return_value = cpp_params
        cpp_cell.persons.return_value = [cpp_person] * 5

        cpp_inf = mock.PropertyMock(return_value=1)
        type(cpp_params).infectiousness = cpp_inf
        cpp_next_status = mock.PropertyMock()
        type(cpp_params).next_status = cpp_next_status

        self.cpp_fac.make_empty_population.return_value = cpp_pop
        self.cpp_map.__getitem__.side_effect = lambda x: getattr(self.cpp_map,
                                                                 str(x))

        # Modify python pop to add additional people with all infection stati
        self.microcell.add_people(3)
        for i, status in enumerate([InfectionStatus.Susceptible,
                                    InfectionStatus.Exposed,
                                    InfectionStatus.Recovered,
                                    InfectionStatus.Dead,
                                    InfectionStatus.InfectMild]):
            self.microcell.persons[i].update_status(status)
        self.microcell.persons[-1].next_infection_status = \
            InfectionStatus.Recovered

        with self.assertRaises(NotImplementedError):
            _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)

        cpp_pop.get_cell.assert_called_once_with(0)
        cpp_cell.index.assert_called_once_with()

        self.assertEqual(cpp_person.params.call_count,
                         len(cpp_cell.persons.return_value))
        self.assertEqual(cpp_inf.call_count,
                         len(cpp_cell.persons.return_value))
        cpp_next_status.assert_called_once_with(
            self.cpp_map[InfectionStatus.Recovered])

        cpp_cell.mark_non_infectious.assert_called_once_with(0)
        cpp_cell.mark_exposed.assert_called_once_with(0)
        cpp_cell.mark_recovered.assert_called_once_with(0)
        cpp_cell.mark_dead.assert_called_once_with(0)
        cpp_cell.mark_infectious.assert_called_once_with(0)

        self.assertIn('_configure_people took',
                      mock_print.call_args_list[-1][0][0])

    @mock.patch(converter_path + '._link_places')
    @mock.patch('builtins.print')
    def test_configure_households(self, mock_print, mock_link):
        mock_link.side_effect = NotImplementedError()
        cpp_mcell, cpp_cell, cpp_pop = self.generate_cpp_mocked_pop()
        cpp_cell.persons.return_value = [mock.Mock()] * 2
        self.cpp_fac.make_empty_population.return_value = cpp_pop

        # Create multiple person house
        self.house.persons.append(self.persons[1])
        self.persons[1].household = self.house

        cpp_household = mock.Mock()
        cpp_params = mock.MagicMock()
        cpp_household.params.return_value = cpp_params
        cpp_mcell.get_household.return_value = cpp_household

        cpp_inf = mock.PropertyMock()
        cpp_location = mock.PropertyMock()
        type(cpp_params).infectiousness = cpp_inf
        type(cpp_params).location = cpp_location

        with self.assertRaises(NotImplementedError):
            _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)

        cpp_mcell.get_household.assert_called_once_with(0)
        cpp_inf.assert_called_once_with(self.house.infectiousness)
        cpp_location.assert_called_once_with(self.house.location)

        self.assertIn('_configure_households took',
                      mock_print.call_args_list[-1][0][0])

    @mock.patch(converter_path + '._link_places')
    @mock.patch('builtins.print')
    def test_handle_neighbours(self, mock_print, mock_link):
        cpp_mcell, cpp_cell, cpp_pop = self.generate_cpp_mocked_pop()
        cpp_cell.persons.return_value = [mock.Mock()] * 2
        self.cpp_fac.make_empty_population.return_value = cpp_pop

        # Add 'neighbour' to population - i.e. two households in one microcell
        self.new_house = pe.Household(self.microcell, [1.0, 1.0])
        self.new_house.persons = [self.persons[1]]
        self.persons[1].household = self.new_house

        cpp_household = mock.Mock()
        cpp_mcell.get_household.return_value = cpp_household
        _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)

        mock_link.assert_called_once_with()
        self.assertIn('_configure_households took',
                      mock_print.call_args_list[-1][0][0])

    @mock.patch(converter_path + '._link_places')
    @mock.patch('builtins.print')
    def test_catch_misconfigured_households(self, _, mock_link):
        cpp_mcell, cpp_cell, cpp_pop = self.generate_cpp_mocked_pop()
        cpp_cell.persons.return_value = [mock.Mock()] * 2
        self.cpp_fac.make_empty_population.return_value = cpp_pop

        cpp_household = mock.Mock()
        cpp_mcell.get_household.return_value = cpp_household

        # Modify household set to add person to multiple households
        second_house = pe.Household(self.microcell, [1.0, 1.0])
        second_house.persons = [self.persons[0]]  # Now in two households

        cpp_person = mock.Mock()
        cpp_person.set_household.return_value = False
        cpp_cell.get_person.return_value = cpp_person

        with self.assertRaises(AssertionError) as context:
            _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)
        mock_link.assert_not_called()  # As unhandled error thrown before this

        cpp_person.set_household.assert_called_once_with(0)
        err_msg = "Person was already in a different household."
        self.assertEqual(context.exception.args[0], err_msg)

    @mock.patch('builtins.print')
    def test_link_places(self, mock_print):
        _, cpp_cell, cpp_pop = self.generate_cpp_mocked_pop()
        cpp_cell.persons.return_value = [mock.Mock()] * 2
        self.cpp_fac.make_empty_population.return_value = cpp_pop

        cpp_place = mock.Mock()
        cpp_place.index.return_value = 0
        cpp_pop.get_place.return_value = cpp_place

        _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)
        cpp_pop.get_place.assert_called_once_with(0)

        self.assertIn('_link_places took',
                      mock_print.call_args_list[-1][0][0])

    @mock.patch('builtins.print')
    def test_mis_indexed_places(self, _):
        _, cpp_cell, cpp_pop = self.generate_cpp_mocked_pop()
        cpp_cell.persons.return_value = [mock.Mock()] * 2
        self.cpp_fac.make_empty_population.return_value = cpp_pop

        cpp_place = mock.Mock()
        cpp_place.index.return_value = 1
        cpp_pop.get_place.return_value = cpp_place

        with self.assertRaises(AssertionError):
            _py2c_converter(self.pop, self.cpp_fac, self.cpp_map)


if __name__ == '__main__':
    unittest.main()
