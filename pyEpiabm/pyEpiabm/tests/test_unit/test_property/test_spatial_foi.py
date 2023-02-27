import unittest
from unittest.mock import patch

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus, SpatialInfection
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestSpatialInfection(TestPyEpiabm):
    """Test the 'PlaceInfection' class, which contains the
    infectiousness and susceptibility calculations that
    determine whether infection events occur within places.
    Each function should return a number greater than 0.
    """

    def setUp(self) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        super(TestSpatialInfection, self).setUpClass()  # Sets up parameters
        self._population = pe.Population()
        self._population.add_cells(1)
        self._population.cells[0].add_microcells(1)
        self._population.cells[0].microcells[0].add_people(2)
        for person in self._population.cells[0].microcells[0].persons:
            person.update_status(InfectionStatus(7))
        self.cell = self._population.cells[0]
        self.infector = self.cell.microcells[0].persons[0]
        self.infectee = self.cell.microcells[0].persons[1]
        self.infector.infectiousness = 1.0
        self.time = 1.0
        pe.Parameters.instance().basic_reproduction_num = 2.8

    def test_spatial_susc(self):
        result = SpatialInfection.spatial_susc(
            self.cell, self.infector, self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    @patch('pyEpiabm.core.Parameters.instance')
    def test_spatial_susc_no_age(self, mock_params):
        mock_params.return_value.use_ages = False
        result = SpatialInfection.spatial_susc(
            self.cell, self.infector, self.infectee, self.time)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_spatial_inf(self):
        result = SpatialInfection.spatial_inf(
            self.cell, self.infector, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    @patch('pyEpiabm.core.Parameters.instance')
    def test_spatial_inf_no_age(self, mock_params):
        mock_params.return_value.use_ages = False
        result = SpatialInfection.spatial_inf(
            self.cell, self.infector, self.time)
        self.assertIsInstance(result, float)
        self.assertEqual(result, self.infector.infectiousness)

    def test_spatial_foi(self):
        result = SpatialInfection.spatial_foi(
            self.cell, self.cell,
            self.infector, self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_cell_inf(self):
        self.infector.update_status(InfectionStatus.InfectMild)
        result = SpatialInfection.cell_inf(self.cell,
                                           self.time)
        self.assertIsInstance(result, float)
        self.assertTrue(result >= 0)

    def test_spatial_case_isolation(self):
        # Not isolating (isolation_start_time = None)
        result = SpatialInfection.spatial_foi(
            self.cell, self.cell,
            self.infector, self.infectee, self.time)

        # Case isolate
        isolation_effectiveness = \
            pe.Parameters.instance().intervention_params['case_isolation'][
                'isolation_effectiveness']
        self.infector.isolation_start_time = 1
        result_isolating = SpatialInfection.spatial_foi(
            self.cell, self.cell,
            self.infector, self.infectee, self.time)
        self.assertEqual(result*isolation_effectiveness,
                         result_isolating)

    def test_spatial_place_closure(self):
        # Not place closure (closure_start_time = None)
        result_susc = SpatialInfection.spatial_susc(
            self.cell, self.infector, self.infectee, self.time)
        result_inf = SpatialInfection.spatial_inf(
            self.cell, self.infector, self.time)

        # Update start time
        closure_spatial_params = \
            pe.Parameters.instance().intervention_params[
                'place_closure']['closure_spatial_params']
        self.infector.microcell.closure_start_time = 1

        # Place closure susceptibility
        result_closure_susc = SpatialInfection.spatial_susc(
            self.cell, self.infector, self.infectee, self.time)
        self.assertEqual(result_susc*closure_spatial_params,
                         result_closure_susc)

        # Place closure infectiousness
        result_closure_inf = SpatialInfection.spatial_inf(
            self.cell, self.infector, self.time)
        self.assertEqual(result_inf*closure_spatial_params,
                         result_closure_inf)

    def test_spatial_household_quarantine(self):
        # Not in quarantine (quarantine_start_time = None)
        result = SpatialInfection.spatial_foi(
            self.cell, self.cell,
            self.infector, self.infectee, self.time)

        quarantine_spatial_effectiveness = \
            pe.Parameters.instance().intervention_params[
                'household_quarantine']['quarantine_spatial_effectiveness']
        self.infector.quarantine_start_time = 1
        result_isolating = SpatialInfection.spatial_foi(
            self.cell, self.cell,
            self.infector, self.infectee, self.time)
        # foi scaled twice: infectiousness and susceptibility
        self.assertEqual(result*quarantine_spatial_effectiveness
                         * quarantine_spatial_effectiveness,
                         result_isolating)

    def test_spatial_social_distancing(self):
        # Not in social distancing (distancing_start_time = None)
        result = SpatialInfection.spatial_susc(
            self.cell, self.infector, self.infectee, self.time)

        # Normal social distancing
        self.infector.microcell.distancing_start_time = 1
        self.infector.distancing_enhanced = False
        distancing_spatial_susc = pe.Parameters.instance().\
            intervention_params['social_distancing'][
                'distancing_spatial_susc']
        result_distancing = SpatialInfection.spatial_susc(
            self.cell, self.infector, self.infectee, self.time)
        self.assertEqual(result*distancing_spatial_susc,
                         result_distancing)

        # Enhanced social distancing
        self.infector.distancing_enhanced = True
        distancing_spatial_enhanced_susc = pe.Parameters.instance().\
            intervention_params['social_distancing'][
                'distancing_spatial_enhanced_susc']
        result_distancing_enhanced = SpatialInfection.spatial_susc(
            self.cell, self.infector, self.infectee, self.time)
        self.assertEqual(result*distancing_spatial_enhanced_susc,
                         result_distancing_enhanced)


if __name__ == '__main__':
    unittest.main()
