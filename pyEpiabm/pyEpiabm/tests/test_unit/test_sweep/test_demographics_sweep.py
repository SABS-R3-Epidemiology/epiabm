import os
from unittest.mock import patch, mock_open

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestDemographicsSweep(TestPyEpiabm):
    """Tests the 'DemographicsSweep' class.
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
        self.file_params = {"output_dir":
                            "pyEpiabm/pyEpiabm/tests/test_output/mock"}

    @patch('os.makedirs')
    def test_construct(self, mock_mkdir):
        # Check faulty input
        self.assertRaises(ValueError, pe.sweep.DemographicsSweep, {})

        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            # Now test init using valid input
            dem_sweep = pe.sweep.DemographicsSweep(self.file_params)
            dem_sweep.bind_population(self.test_population)
            self.assertEqual(dem_sweep.spatial_output, False)
            self.assertEqual(dem_sweep.age_output, False)
            file_name = os.path.join(os.getcwd(),
                                     self.file_params["output_dir"],
                                     "demographics.csv")
            self.assertEqual(dem_sweep.titles, ["id", "kw_or_chr"])
            del dem_sweep.writer
        mo.assert_called_with(file_name, 'w')

        self.file_params["spatial_output"] = True
        self.file_params["age_output"] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            # Now test init using valid input
            dem_sweep = pe.sweep.DemographicsSweep(self.file_params)
            dem_sweep.bind_population(self.test_population)
            self.assertEqual(dem_sweep.spatial_output, True)
            self.assertEqual(dem_sweep.age_output, True)
            file_name = os.path.join(os.getcwd(),
                                     self.file_params["output_dir"],
                                     "demographics.csv")
            self.assertEqual(dem_sweep.titles, ["id", "age_group",
                                                "location_x", "location_y",
                                                "kw_or_chr"])
            del dem_sweep.writer
        mo.assert_called_with(file_name, 'w')

    @patch('os.makedirs')
    def test_write_to_file(self, mock_mkdir):

        if os.path.exists(self.file_params["output_dir"]):
            os.rmdir(self.file_params["output_dir"])

        mo = mock_open()
        self.file_params['spatial_output'] = False
        self.file_params['age_output'] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            dem_sweep = pe.sweep.DemographicsSweep(self.file_params)
            dem_sweep.bind_population(self.test_population)
            person_0_0_0_0_data = {"id": "0.0.0.0", "kw_or_chr": 'K'}
            person_1_0_0_0_data = {"id": "1.0.0.0", "kw_or_chr": 'C'}
            person_1_0_0_1_data = {"id": "1.0.0.1", "kw_or_chr": 'X'}
            with patch.object(dem_sweep.writer, 'write') as mock:
                dem_sweep()
                mock.assert_any_call(person_0_0_0_0_data)
                mock.assert_any_call(person_1_0_0_0_data)
                mock.assert_any_call(person_1_0_0_1_data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.file_params[
                                                       "output_dir"]))

        self.file_params['age_output'] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            dem_sweep = pe.sweep.DemographicsSweep(self.file_params)
            dem_sweep.bind_population(self.test_population)
            person_0_0_0_0_data = {"id": "0.0.0.0", "age_group": 5,
                                   "kw_or_chr": 'K'}
            person_1_0_0_0_data = {"id": "1.0.0.0", "age_group": 13,
                                   "kw_or_chr": 'C'}
            person_1_0_0_1_data = {"id": "1.0.0.1", "age_group": 8,
                                   "kw_or_chr": 'X'}
            with patch.object(dem_sweep.writer, 'write') as mock:
                dem_sweep()
                mock.assert_any_call(person_0_0_0_0_data)
                mock.assert_any_call(person_1_0_0_0_data)
                mock.assert_any_call(person_1_0_0_1_data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.file_params[
                                                       "output_dir"]))

        self.file_params["spatial_output"] = True
        cell_0_x, cell_0_y = self.test_population.cells[0].location
        cell_1_x, cell_1_y = self.test_population.cells[1].location
        self.file_params["age_output"] = False
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            dem_sweep = pe.sweep.DemographicsSweep(self.file_params)
            dem_sweep.bind_population(self.test_population)
            person_0_0_0_0_data = {"id": "0.0.0.0", "location_x": cell_0_x,
                                   "location_y": cell_0_y, "kw_or_chr": 'K'}
            person_1_0_0_0_data = {"id": "1.0.0.0", "location_x": cell_1_x,
                                   "location_y": cell_1_y, "kw_or_chr": 'C'}
            person_1_0_0_1_data = {"id": "1.0.0.1", "location_x": cell_1_x,
                                   "location_y": cell_1_y, "kw_or_chr": 'X'}
            with patch.object(dem_sweep.writer, 'write') as mock:
                dem_sweep()
                mock.assert_any_call(person_0_0_0_0_data)
                mock.assert_any_call(person_1_0_0_0_data)
                mock.assert_any_call(person_1_0_0_1_data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.file_params[
                                                       "output_dir"]))

        self.file_params["age_output"] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            dem_sweep = pe.sweep.DemographicsSweep(self.file_params)
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
                mock.assert_any_call(person_0_0_0_0_data)
                mock.assert_any_call(person_1_0_0_0_data)
                mock.assert_any_call(person_1_0_0_1_data)
        mock_mkdir.assert_called_with(os.path.join(os.getcwd(),
                                                   self.file_params[
                                                       "output_dir"]))
