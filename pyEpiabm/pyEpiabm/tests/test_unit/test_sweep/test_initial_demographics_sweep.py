import os
from unittest.mock import patch, mock_open, call

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestInitialDemographicsSweep(TestPyEpiabm):
    """Tests the 'InitialDemographicsSweep' class.
    """

    def setUp(self) -> None:

        # Setting up a population with three people across 2 cells,
        # 2 microcells and 2 households
        self.test_population = pe.Population()
        self.test_population.add_cells(2)
        self.test_population.cells[0].add_microcells(1)
        self.test_population.cells[0].microcells[0].add_people(1)
        self.test_population.cells[1].add_microcells(1)
        self.test_population.cells[1].microcells[0].add_people(2)
        microcell_0_0 = self.test_population.cells[0].microcells[0]
        microcell_0_0.add_household([microcell_0_0.persons[0]])
        person_0_0_0_0 = microcell_0_0.households[0].persons[0]
        person_0_0_0_0.age_group = 5
        person_0_0_0_0.key_worker = True
        microcell_1_0 = self.test_population.cells[1].microcells[0]
        microcell_1_0.add_household([microcell_1_0.persons[0],
                                     microcell_1_0.persons[1]])
        person_1_0_0_0 = microcell_1_0.households[0].persons[0]
        person_1_0_0_0.age_group = 13
        person_1_0_0_0.care_home_resident = True
        person_1_0_0_1 = microcell_1_0.households[0].persons[1]
        person_1_0_0_1.age_group = 8
        self.dem_file_params = {"output_dir":
                                "pyEpiabm/pyEpiabm/tests/test_output/mock"}

    @patch('os.makedirs')
    def test_construct_invalid_input(self, mock_mkdir):
        # Check faulty input
        with self.assertRaises(ValueError) as cm_1:
            pe.sweep.InitialDemographicsSweep({})
        self.assertEqual("output_dir must be specified in dem_file_params",
                         str(cm_1.exception))

        # Check for invalid keys
        test_dem_file_params = {"output_dir":
                                "pyEpiabm/pyEpiabm/tests/test_output/mock",
                                "age_output": True,
                                "invalid_key": True}
        with self.assertRaises(ValueError) as cm_2:
            pe.sweep.InitialDemographicsSweep(test_dem_file_params)
        self.assertEqual("dem_file_params contains invalid keys: "
                         "{'invalid_key'}", str(cm_2.exception))

        # Check that age_stratified cannot be True while use_ages is False
        del test_dem_file_params["invalid_key"]
        pe.core.Parameters.instance().use_ages = False
        with self.assertRaises(ValueError) as cm_3:
            pe.sweep.InitialDemographicsSweep(test_dem_file_params)
        self.assertEqual("age_output cannot be True as Parameters"
                         ".instance().use_ages is False",
                         str(cm_3.exception))
        pe.core.Parameters.instance().use_ages = True

    @patch('os.makedirs')
    def test_construct(self, mock_mkdir):
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            # Now test init using valid input
            dem_sweep = pe.sweep.InitialDemographicsSweep(self.dem_file_params)
            dem_sweep.bind_population(self.test_population)
            self.assertEqual(dem_sweep.spatial_output, False)
            self.assertEqual(dem_sweep.age_output, False)
            file_name = os.path.join(os.getcwd(),
                                     self.dem_file_params["output_dir"],
                                     "demographics.csv")
            self.assertEqual(dem_sweep.titles, ["id", "kw_or_chr"])
            del dem_sweep.writer
        mo.assert_called_with(file_name, 'w')

        self.dem_file_params["spatial_output"] = True
        self.dem_file_params["age_output"] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            # Now test init using valid input
            dem_sweep = pe.sweep.InitialDemographicsSweep(self.dem_file_params)
            dem_sweep.bind_population(self.test_population)
            self.assertEqual(dem_sweep.spatial_output, True)
            self.assertEqual(dem_sweep.age_output, True)
            file_name = os.path.join(os.getcwd(),
                                     self.dem_file_params["output_dir"],
                                     "demographics.csv")
            self.assertEqual(dem_sweep.titles, ["id", "age_group",
                                                "location_x", "location_y",
                                                "kw_or_chr"])
            del dem_sweep.writer
        mo.assert_called_with(file_name, 'w')

    @patch('os.makedirs')
    def test_write_to_file_no_age_no_spatial(self, mock_mkdir):

        if os.path.exists(self.dem_file_params["output_dir"]):
            os.rmdir(self.dem_file_params["output_dir"])

        mo = mock_open()
        self.dem_file_params['spatial_output'] = False
        self.dem_file_params['age_output'] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            dem_sweep = pe.sweep.InitialDemographicsSweep(self.dem_file_params)
            dem_sweep.bind_population(self.test_population)
            person_0_0_0_0_data = {"id": "0.0.0.0", "kw_or_chr": 'K'}
            person_1_0_0_0_data = {"id": "1.0.0.0", "kw_or_chr": 'C'}
            person_1_0_0_1_data = {"id": "1.0.0.1", "kw_or_chr": 'X'}
            with patch.object(dem_sweep.writer, 'write') as mock:
                dem_sweep()
                mock.assert_has_calls([call(person_0_0_0_0_data),
                                       call(person_1_0_0_0_data),
                                       call(person_1_0_0_1_data)])
                self.assertEqual(mock.call_count, 3)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.dem_file_params[
                                                       "output_dir"]))

    @patch('os.makedirs')
    def test_write_to_file_age_no_spatial(self, mock_mkdir):

        if os.path.exists(self.dem_file_params["output_dir"]):
            os.rmdir(self.dem_file_params["output_dir"])

        mo = mock_open()
        self.dem_file_params['spatial_output'] = False
        self.dem_file_params['age_output'] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            dem_sweep = pe.sweep.InitialDemographicsSweep(self.dem_file_params)
            dem_sweep.bind_population(self.test_population)
            person_0_0_0_0_data = {"id": "0.0.0.0", "age_group": 5,
                                   "kw_or_chr": 'K'}
            person_1_0_0_0_data = {"id": "1.0.0.0", "age_group": 13,
                                   "kw_or_chr": 'C'}
            person_1_0_0_1_data = {"id": "1.0.0.1", "age_group": 8,
                                   "kw_or_chr": 'X'}
            with patch.object(dem_sweep.writer, 'write') as mock:
                dem_sweep()
                mock.assert_has_calls([call(person_0_0_0_0_data),
                                       call(person_1_0_0_0_data),
                                       call(person_1_0_0_1_data)])
                self.assertEqual(mock.call_count, 3)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.dem_file_params[
                                                       "output_dir"]))

    @patch('os.makedirs')
    def test_write_to_file_no_age_spatial(self, mock_mkdir):

        if os.path.exists(self.dem_file_params["output_dir"]):
            os.rmdir(self.dem_file_params["output_dir"])

        mo = mock_open()
        self.dem_file_params['spatial_output'] = True
        self.dem_file_params['age_output'] = False
        cell_0_x, cell_0_y = self.test_population.cells[0].location
        cell_1_x, cell_1_y = self.test_population.cells[1].location
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            dem_sweep = pe.sweep.InitialDemographicsSweep(self.dem_file_params)
            dem_sweep.bind_population(self.test_population)
            person_0_0_0_0_data = {"id": "0.0.0.0", "location_x": cell_0_x,
                                   "location_y": cell_0_y, "kw_or_chr": 'K'}
            person_1_0_0_0_data = {"id": "1.0.0.0", "location_x": cell_1_x,
                                   "location_y": cell_1_y, "kw_or_chr": 'C'}
            person_1_0_0_1_data = {"id": "1.0.0.1", "location_x": cell_1_x,
                                   "location_y": cell_1_y, "kw_or_chr": 'X'}
            with patch.object(dem_sweep.writer, 'write') as mock:
                dem_sweep()
                mock.assert_has_calls([call(person_0_0_0_0_data),
                                       call(person_1_0_0_0_data),
                                       call(person_1_0_0_1_data)])
                self.assertEqual(mock.call_count, 3)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.dem_file_params[
                                                       "output_dir"]))

    @patch('os.makedirs')
    def test_write_to_file_age_spatial(self, mock_mkdir):

        if os.path.exists(self.dem_file_params["output_dir"]):
            os.rmdir(self.dem_file_params["output_dir"])

        mo = mock_open()
        self.dem_file_params['spatial_output'] = True
        self.dem_file_params['age_output'] = True
        cell_0_x, cell_0_y = self.test_population.cells[0].location
        cell_1_x, cell_1_y = self.test_population.cells[1].location
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            dem_sweep = pe.sweep.InitialDemographicsSweep(self.dem_file_params)
            dem_sweep.bind_population(self.test_population)
            person_0_0_0_0_data = {"id": "0.0.0.0", "age_group": 5,
                                   "location_x": cell_0_x,
                                   "location_y": cell_0_y, "kw_or_chr": 'K'}
            person_1_0_0_0_data = {"id": "1.0.0.0", "age_group": 13,
                                   "location_x": cell_1_x,
                                   "location_y": cell_1_y, "kw_or_chr": 'C'}
            person_1_0_0_1_data = {"id": "1.0.0.1", "age_group": 8,
                                   "location_x": cell_1_x,
                                   "location_y": cell_1_y, "kw_or_chr": 'X'}
            with patch.object(dem_sweep.writer, 'write') as mock:
                dem_sweep()
                mock.assert_has_calls([call(person_0_0_0_0_data),
                                       call(person_1_0_0_0_data),
                                       call(person_1_0_0_1_data)])
                self.assertEqual(mock.call_count, 3)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.dem_file_params[
                                                       "output_dir"]))
