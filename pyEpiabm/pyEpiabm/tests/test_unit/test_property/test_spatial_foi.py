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
        self.infector = self._population.cells[0].microcells[0].persons[0]
        self.infectee = self._population.cells[0].microcells[0].persons[1]
        self.infector.infectiousness = 1.0
        self.time = 1.0
        pe.Parameters.instance().basic_reproduction_num = 2.8

    def test_spatial_susc(self):
        result = SpatialInfection.spatial_susc(
            self._population.cells[0], self.infector, self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    @patch('pyEpiabm.core.Parameters.instance')
    def test_spatial_susc_no_age(self, mock_params):
        mock_params.return_value.use_ages = False
        result = SpatialInfection.spatial_susc(
            self._population.cells[0], self.infector, self.infectee, self.time)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_spatial_inf(self):
        result = SpatialInfection.spatial_inf(
            self._population.cells[0], self.infector, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    @patch('pyEpiabm.core.Parameters.instance')
    def test_spatial_inf_no_age(self, mock_params):
        mock_params.return_value.use_ages = False
        result = SpatialInfection.spatial_inf(
            self._population.cells[0], self.infector, self.time)
        self.assertIsInstance(result, float)
        self.assertEqual(result, self.infector.infectiousness)

    def test_spatial_foi(self):
        result = SpatialInfection.spatial_foi(
            self._population.cells[0], self._population.cells[0],
            self.infector, self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_cell_inf(self):
        self.infector.update_status(InfectionStatus.InfectMild)
        result = SpatialInfection.cell_inf(self._population.cells[0],
                                           self.time)
        self.assertIsInstance(result, float)
        self.assertTrue(result >= 0)

    def test_spatial_case_isolation(self):
        result = SpatialInfection.spatial_foi(
            self._population.cells[0], self._population.cells[0],
            self.infector, self.infectee, self.time)

        # Case isolate
        isolation_effectiveness = 0.5
        pe.Parameters.instance().intervention_params['case_isolation'][
            'isolation_effectiveness'] = isolation_effectiveness
        self.infector.isolation_start_time = 1
        result_isolating = SpatialInfection.spatial_foi(
            self._population.cells[0], self._population.cells[0],
            self.infector, self.infectee, self.time)
        self.assertEqual(result*isolation_effectiveness,
                         result_isolating)

    def test_spatial_place_closure(self):
        result_susc = SpatialInfection.spatial_susc(
            self._population.cells[0], self.infector, self.infectee, self.time)
        result_inf = SpatialInfection.spatial_inf(
            self._population.cells[0], self.infector, self.time)

        # Update start time
        closure_spatial_params = 0.5
        self.infector.microcell.closure_start_time = 1

        # Place closure susceptibility
        result_closure_susc = SpatialInfection.spatial_susc(
            self._population.cells[0], self.infector, self.infectee, self.time)
        self.assertEqual(result_susc*closure_spatial_params,
                         result_closure_susc)

        # Place closure infectiousness
        result_closure_inf = SpatialInfection.spatial_inf(
            self._population.cells[0], self.infector, self.time)
        self.assertEqual(result_inf*closure_spatial_params,
                         result_closure_inf)

    def test_spatial_household_quarantine(self):
        result = SpatialInfection.spatial_foi(
            self._population.cells[0], self._population.cells[0],
            self.infector, self.infectee, self.time)
        quarantine_spatial_effectiveness = 0.5
        pe.Parameters.instance().intervention_params['household_quarantine'][
            'quarantine_spatial_effectiveness'] =\
            quarantine_spatial_effectiveness
        self.infector.quarantine_start_time = 1
        result_isolating = SpatialInfection.spatial_foi(
            self._population.cells[0], self._population.cells[0],
            self.infector, self.infectee, self.time)
        # foi scaled twice: infectiousness and susceptibility
        self.assertEqual(result*quarantine_spatial_effectiveness
                         * quarantine_spatial_effectiveness,
                         result_isolating)


if __name__ == '__main__':
    unittest.main()
