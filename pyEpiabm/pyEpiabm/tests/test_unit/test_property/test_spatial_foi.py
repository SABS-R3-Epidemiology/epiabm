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

    def setUp(self) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        super(TestSpatialInfection, self).setUpClass()  # Sets up parameters
        self._population = pe.Population()
        self._population.add_cells(1)
        self._population.cells[0].add_microcells(1)
        self.microcell = self._population.cells[0].microcells[0]
        self.microcell.add_place(1, (1, 1), PlaceType.CareHome)
        self.microcell.add_people(2)
        for person in self._population.cells[0].microcells[0].persons:
            person.update_status(InfectionStatus(7))
        self.cell = self._population.cells[0]
        self.infector = self.microcell.persons[0]
        self.infectee = self.microcell.persons[1]
        self.infector.infectiousness = 1.0
        self.time = 1.0
        pe.Parameters.instance().basic_reproduction_num = 2.8

    def test_spatial_susc(self):
        result = SpatialInfection.spatial_susc(
            self.cell, self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    @patch('pyEpiabm.core.Parameters.instance')
    def test_spatial_susc_no_age(self, mock_params):
        mock_params.return_value.use_ages = False
        result = SpatialInfection.spatial_susc(
            self.cell, self.infectee, self.time)
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
        # Update place type, not place closure (closure_start_time = None)
        self.infectee.place_types.append(PlaceType.PrimarySchool)
        self.infector.place_types.append(PlaceType.Workplace)
        result_susc = SpatialInfection.spatial_susc(
            self.cell, self.infectee, self.time)
        result_inf = SpatialInfection.spatial_inf(
            self.cell, self.infector, self.time)

        # Update start time
        closure_spatial_params = \
            pe.Parameters.instance().intervention_params[
                'place_closure']['closure_spatial_params']
        self.infectee.microcell.closure_start_time = 1

        # Place closure susceptibility of infectee
        pe.Parameters.instance().intervention_params[
            'place_closure']['closure_place_type'] = [1, 2, 3, 4, 5, 6]
        result_closure_susc = SpatialInfection.spatial_susc(
            self.cell, self.infectee, self.time)
        self.assertEqual(result_susc*closure_spatial_params,
                         result_closure_susc)

        # Place closure infectiousness of infector
        pe.Parameters.instance().intervention_params[
            'place_closure']['closure_place_type'] = [1, 2, 3, 4, 5, 6]
        result_closure_inf = SpatialInfection.spatial_inf(
            self.cell, self.infector, self.time)
        self.assertEqual(result_inf*closure_spatial_params,
                         result_closure_inf)

        # Place closure foi, place of infectee and infector closed
        pe.Parameters.instance().intervention_params[
            'place_closure']['closure_place_type'] = [1, 2, 3, 4, 5, 6]
        result_closure_foi = SpatialInfection.spatial_foi(
            self.cell, self.cell, self.infector, self.infectee, self.time)
        self.assertEqual(result_susc*closure_spatial_params*result_inf*closure_spatial_params,
                         result_closure_foi)

        # Place closure foi, place of only infectee closed
        pe.Parameters.instance().intervention_params['place_closure']['closure_place_type'] = [1, 2, 3]
        result_closure_foi = SpatialInfection.spatial_foi(
            self.cell, self.cell, self.infector, self.infectee, self.time)
        self.assertEqual(result_susc*result_inf*closure_spatial_params,
                         result_closure_foi)

    def test_spatial_household_quarantine(self):
        # Not in quarantine (quarantine_start_time = None)
        result = SpatialInfection.spatial_foi(
            self.cell, self.cell,
            self.infector, self.infectee, self.time)

        quarantine_spatial_effectiveness = \
            pe.Parameters.instance().intervention_params[
                'household_quarantine']['quarantine_spatial_effectiveness']
        self.infectee.quarantine_start_time = 1
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
            self.cell, self.infectee, self.time)

        # Normal social distancing
        self.infector.microcell.distancing_start_time = 1
        self.infector.distancing_enhanced = False
        distancing_spatial_susc = pe.Parameters.instance().\
            intervention_params['social_distancing'][
                'distancing_spatial_susc']
        result_distancing = SpatialInfection.spatial_susc(
            self.cell, self.infectee, self.time)
        self.assertEqual(result*distancing_spatial_susc,
                         result_distancing)

        # Enhanced social distancing of infectee
        self.infectee.distancing_enhanced = True
        distancing_spatial_enhanced_susc = pe.Parameters.instance().\
            intervention_params['social_distancing'][
                'distancing_spatial_enhanced_susc']
        result_distancing_enhanced = SpatialInfection.spatial_susc(
            self.cell, self.infectee, self.time)
        self.assertEqual(result*distancing_spatial_enhanced_susc,
                         result_distancing_enhanced)

    def test_spatial_travel_isolation(self):
        # Not travel isolating (travel_isolation_start_time = None)
        result = SpatialInfection.spatial_foi(
            self.cell, self.cell,
            self.infector, self.infectee, self.time)

        # Case isolate
        isolation_effectiveness = pe.Parameters.instance().intervention_params[
            'travel_isolation']['isolation_effectiveness']
        self.infector.isolation_start_time = 1
        self.infector.travel_isolation_start_time = 1
        result_isolating = SpatialInfection.spatial_foi(
            self.cell, self.cell, self.infector, self.infectee, self.time)
        self.assertEqual(result*isolation_effectiveness,
                         result_isolating)

    @patch('pyEpiabm.property.SpatialInfection.spatial_susc')
    @patch('pyEpiabm.property.SpatialInfection.spatial_inf')
    @patch('pyEpiabm.core.Parameters.instance')
    def test_carehome_scaling(self, mock_params, mock_inf, mock_susc):
        mock_inf.return_value = 1
        mock_susc.return_value = 1
        mock_params.return_value.carehome_params\
            = {'carehome_resident_spatial_scaling': 2}
        self.infector.care_home_resident = True
        self.infectee.care_home_resident = False
        result = SpatialInfection.spatial_foi(self.cell, self.cell,
                                              self.infector, self.infectee,
                                              self.time)
        self.assertEqual(result, 4)

        self.infector.care_home_resident = False
        self.infectee.care_home_resident = True
        result = SpatialInfection.spatial_foi(self.cell, self.cell,
                                              self.infector, self.infectee,
                                              self.time)
        self.assertEqual(result, 2)

        self.infector.care_home_resident = True
        self.infectee.care_home_resident = True
        result = SpatialInfection.spatial_foi(self.cell, self.cell,
                                              self.infector, self.infectee,
                                              self.time)
        self.assertEqual(result, 4)

        self.assertEqual(mock_inf.call_count, 3)
        self.assertEqual(mock_susc.call_count, 3)


if __name__ == '__main__':
    unittest.main()
