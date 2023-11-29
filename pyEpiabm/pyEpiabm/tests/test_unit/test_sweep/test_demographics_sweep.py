import os
import unittest
from unittest.mock import patch, mock_open

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestDemographicsSweep(TestPyEpiabm):
    """Tests the 'DemographicsSweep' class.
    """

    def setUp(self) -> None:
        self.test_population = pe.Population()
        self.test_population.add_cells(2)
        self.test_population.cells[0].add_microcells(1)
        self.test_population.cells[1].add_microcells(3)
        microcell_0_0 = self.test_population.cells[0].microcells[0]
        microcell_0_0.add_household([pe.Person(microcell_0_0)])
        first_person = microcell_0_0.households[0].persons[0]
        first_person.age = 5
        first_person.key_worker = True
        microcell_1_0 = self.test_population.cells[1].microcells[0]
        microcell_1_0.add_household([pe.Person(microcell_1_0),
                                     pe.Person(microcell_1_0)])
        microcell_1_0.add_household([pe.Person(microcell_1_0)])
        microcell_1_1 = self.test_population.cells[1].microcells[1]
        microcell_1_1.add_household([pe.Person(microcell_1_1)])
        microcell_1_1.add_household([pe.Person(microcell_1_1)])
        microcell_1_2 = self.test_population.cells[1].microcells[2]
        microcell_1_2.add_household([pe.Person(microcell_1_2),
                                     pe.Person(microcell_1_2),
                                     pe.Person(microcell_1_2)])
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
            self.assertEqual(dem_sweep.spatial_output, False)
            self.assertEqual(dem_sweep.age_output, False)
            file_name = os.path.join(os.getcwd(),
                                     self.file_params["output_dir"],
                                     "demographics.csv")
            self.assertEqual(dem_sweep.titles, ["id", "kw_or_chr"])
            del dem_sweep.writer
        mo.assert_called_with(file_name, 'w')

        self.file_params["spatial_output"] = True
        self.file_params["age_stratified"] = True
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            # Now test init using valid input
            dem_sweep = pe.sweep.DemographicsSweep(self.file_params)
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
