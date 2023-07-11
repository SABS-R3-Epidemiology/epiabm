import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import InterventionSweep
from pyEpiabm.intervention import CaseIsolation, HouseholdQuarantine, \
    PlaceClosure, SocialDistancing, DiseaseTesting, TravelIsolation
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestInterventionSweep(TestPyEpiabm):
    """Test the 'InterventionSweep' class.
    """

    def setUp(self) -> None:

        # Construct a sequence of place closure
        pe.Parameters.instance().intervention_params['place_closure'] = [
            pe.Parameters.instance().intervention_params[
                'place_closure'].copy() for _ in range(2)]
        pe.Parameters.instance().intervention_params[
            'place_closure'][1]['start_time'] = 400
        pe.Parameters.instance().intervention_params[
            'place_closure'][1]['closure_place_type'] = [1, 2, 3, 4, 5]
        self.intervention_sweep = InterventionSweep()

        # Construct a population with 2 persons, one infector and one infectee
        self.pop_factory = pe.routine.ToyPopulationFactory()
        self.pop_params = {"population_size": 2, "cell_number": 1,
                           "microcell_number": 1, "household_number": 1}
        self._population = self.pop_factory.make_pop(self.pop_params)
        self._microcell = self._population.cells[0].microcells[0]
        self.person_susc = self._microcell.persons[0]
        self.person_susc.update_status(InfectionStatus(1))
        self.person_symp = self._microcell.persons[1]
        self.person_symp.update_status(InfectionStatus(4))

        # cls.intervention_sweep.bind_population(cls._population)

    def test_bind_population(self):
        self.intervention_sweep.bind_population(self._population)
        self.assertEqual(len(self.intervention_sweep.
                             intervention_params['case_isolation']), 9)
        self.assertEqual(len(self.intervention_sweep.
                             intervention_params['vaccine_params']), 9)
        self.assertEqual(len(self.intervention_sweep.
                             intervention_params['place_closure']), 2)
        self.assertEqual(len(pe.Parameters.instance().intervention_params[
                            'place_closure']), 9)
        self.assertEqual(len(self.intervention_sweep.
                             intervention_params['household_quarantine']), 10)
        self.assertEqual(len(self.intervention_sweep.
                             intervention_params['social_distancing']), 13)
        self.assertEqual(len(self.intervention_sweep.
                             intervention_params['disease_testing']), 10)
        self.assertEqual(len(self.intervention_sweep.
                             intervention_params['travel_isolation']), 10)
        self.assertEqual(len(
            self.intervention_sweep.intervention_active_status.keys()), 8)

    def test___call__(self):
        self.intervention_sweep.bind_population(self._population)
        self.intervention_sweep(time=10)
        # Interventions are active, except the second place closure
        self.assertTrue(
            self.intervention_sweep.intervention_active_status[
                [key for key in
                 self.intervention_sweep.intervention_active_status.keys()
                 if isinstance(key, CaseIsolation)][0]])
        self.assertTrue(
            self.intervention_sweep.intervention_active_status[
                [key for key in
                 self.intervention_sweep.intervention_active_status.keys()
                 if isinstance(key, HouseholdQuarantine)][0]])
        self.assertTrue(
            self.intervention_sweep.intervention_active_status[
                [key for key in
                 self.intervention_sweep.intervention_active_status.keys()
                 if isinstance(key, PlaceClosure)][0]])
        self.assertFalse(
            self.intervention_sweep.intervention_active_status[
                [key for key in
                 self.intervention_sweep.intervention_active_status.keys()
                 if isinstance(key, PlaceClosure)][1]])
        self.assertTrue(
            self.intervention_sweep.intervention_active_status[
                [key for key in
                 self.intervention_sweep.intervention_active_status.keys()
                 if isinstance(key, SocialDistancing)][0]])
        self.assertTrue(
            self.intervention_sweep.intervention_active_status[
                [key for key in
                 self.intervention_sweep.intervention_active_status.keys()
                 if isinstance(key, DiseaseTesting)][0]])
        self.assertTrue(
            self.intervention_sweep.intervention_active_status[
                [key for key in
                 self.intervention_sweep.intervention_active_status.keys()
                 if isinstance(key, TravelIsolation)][0]])

        # Place is closed and social distancing ends
        self.assertIsNotNone(self.intervention_sweep._population.cells[0].
                             microcells[0].closure_start_time)
        self.assertIsNotNone(self.intervention_sweep._population.cells[0].
                             microcells[0].distancing_start_time)

        # Infector in case isolation, infectee in quarantine as
        # isolation_start_time = 100 as evaluated at this time (see above)
        self.intervention_sweep.intervention_params['case_isolation'][
            'isolation_probability'] = 1.0
        self.intervention_sweep.intervention_params['household_quarantine'][
            'quarantine_house_compliant'] = 1.0
        self.intervention_sweep.intervention_params['household_quarantine'][
            'quarantine_individual_compliant'] = 1.0
        self.assertEqual(self.person_symp.isolation_start_time, 10)
        self.assertIsNotNone(self.person_susc.quarantine_start_time)

        # Parameters for the first place closure
        self.assertEqual(self.intervention_sweep._population.cells[0].
                         microcells[0].closure_start_time, 10)
        self.assertEqual(pe.Parameters.instance().intervention_params[
            'place_closure']['closure_place_type'], [1, 2, 3])

        # Closure_start_time is None after the end of the first place closure
        # and before the start of the second place closure
        self.intervention_sweep(time=120)
        self.assertIsNone(self.intervention_sweep._population.cells[0].
                          microcells[0].closure_start_time)

        # Place closure parameters are changed after activating
        # the second place closure
        self.intervention_sweep(time=400)
        self.assertEqual(self.intervention_sweep._population.cells[0].
                         microcells[0].closure_start_time, 400)
        self.assertEqual(pe.Parameters.instance().intervention_params[
            'place_closure']['closure_place_type'], [1, 2, 3, 4, 5])

        # Stop isolating after start_time + policy_duration
        self.intervention_sweep.intervention_params['case_isolation'][
            'policy_duration'] = 365
        self.person_symp.isolation_start_time = 370
        self.intervention_sweep(time=370)
        self.assertEqual(self.person_symp.isolation_start_time, 370)
        self.intervention_sweep(time=372)
        self.assertFalse(
            self.intervention_sweep.intervention_active_status[
                [key for key in
                 self.intervention_sweep.intervention_active_status.keys()
                 if isinstance(key, CaseIsolation)][0]])
        self.assertIsNone(self.person_symp.isolation_start_time)

    @mock.patch('logging.warning')
    def test_concurrent_event_warning(self, mock_log):
        # Move the second intervention forward in time so it is concurrent
        pe.Parameters.instance().intervention_params[
            'place_closure'][1]['start_time'] = 150
        pe.Parameters.instance().intervention_params[
            'place_closure'][1]['closure_place_type'] = [4, 5]

        # Bind pop to new intervention list to check for concurrency
        self.intervention_sweep.bind_population(self._population)
        self.intervention_sweep(time=260)
        mock_log.assert_called_once_with(
            "Concurrent place_closure interventions should not occur!")
        self.assertEqual(pe.Parameters.instance().intervention_params[
                'place_closure']['closure_place_type'], [4, 5])


if __name__ == '__main__':
    unittest.main()
