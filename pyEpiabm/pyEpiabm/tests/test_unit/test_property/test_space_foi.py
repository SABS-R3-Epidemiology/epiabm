import unittest
from unittest.mock import patch

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus, SpatialInfection, PlaceType
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestSpatialInfection(TestPyEpiabm):
    """Test the 'PlaceInfection' class, which contains the
    infectiousness and susceptibility calculations that
    determine whether infection events occur within places.
    Each function should return a number greater than 0.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        super(TestSpatialInfection, cls).setUpClass()  # Sets up parameters
        cls.cell = pe.Cell()
        cls.cell.add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.microcell.add_place(1, (1, 1), PlaceType.CareHome)
        cls.microcell.add_people(2)
        cls.infector = cls.microcell.persons[0]
        cls.infector.infectiousness = 1.0
        cls.infectee = cls.microcell.persons[1]
        cls.time = 1.0
        pe.Parameters.instance().basic_reproduction_num = 2.8

    def test_space_susc(self):
        result = SpatialInfection.space_susc(self.cell, self.infectee,
                                             self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    @patch('pyEpiabm.core.Parameters.instance')
    def test_space_susc_no_age(self, mock_params):
        mock_params.return_value.use_ages = False
        result = SpatialInfection.space_susc(self.cell, self.infectee,
                                             self.time)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1)

    def test_space_inf(self):
        result = SpatialInfection.space_inf(self.cell, self.infector,
                                            self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    @patch('pyEpiabm.core.Parameters.instance')
    def test_space_inf_no_age(self, mock_params):
        mock_params.return_value.use_ages = False
        result = SpatialInfection.space_inf(self.cell, self.infector,
                                            self.time)
        self.assertIsInstance(result, float)
        self.assertEqual(result, self.infector.infectiousness)

    def test_space_foi(self):
        result = SpatialInfection.space_foi(self.cell, self.cell,
                                            self.infector, self.infectee,
                                            self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_cell_inf(self):
        self.infector.update_status(InfectionStatus.InfectMild)
        result = SpatialInfection.cell_inf(self.cell, self.time)
        self.assertIsInstance(result, float)
        self.assertTrue(result >= 0)

    @patch('pyEpiabm.property.SpatialInfection.space_susc')
    @patch('pyEpiabm.property.SpatialInfection.space_inf')
    @patch('pyEpiabm.core.Parameters.instance')
    def test_carehome_scaling(self, mock_params, mock_inf, mock_susc):
        mock_inf.return_value = 1
        mock_susc.return_value = 1
        mock_params.return_value.carehome_params\
            = {'carehome_resident_spatial_scaling': 2}
        self.infector.care_home_resident = True
        self.infectee.care_home_resident = False
        result = SpatialInfection.space_foi(self.cell, self.cell,
                                            self.infector, self.infectee,
                                            self.time)
        self.assertEqual(result, 4)

        self.infector.care_home_resident = False
        self.infectee.care_home_resident = True
        result = SpatialInfection.space_foi(self.cell, self.cell,
                                            self.infector, self.infectee,
                                            self.time)
        self.assertEqual(result, 2)

        self.infector.care_home_resident = True
        self.infectee.care_home_resident = True
        result = SpatialInfection.space_foi(self.cell, self.cell,
                                            self.infector, self.infectee,
                                            self.time)
        self.assertEqual(result, 4)

if __name__ == '__main__':
    unittest.main()
