import unittest

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import InterventionSweep
from pyEpiabm.intervention import CaseIsolation, HouseholdQuarantine, \
    PlaceClosure, SocialDistancing, DiseaseTesting, TravelIsolation
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestInterventionSweep(TestPyEpiabm):
    """Test the 'InterventionSweep' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super(TestInterventionSweep, cls).setUpClass()

        # Construct a sequence of case isolation
        pe.Parameters.instance().intervention_params['place_closure'] = [
            pe.Parameters.instance().intervention_params[
                'place_closure'].copy(),
            pe.Parameters.instance().intervention_params[
                'place_closure'].copy()]
        pe.Parameters.instance().intervention_params[
            'place_closure'][1]['start_time'] = 200
        cls.interventionsweep = InterventionSweep()

        # Construct a population with 2 persons, one infector and one infectee
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 2, "cell_number": 1,
                          "microcell_number": 1, "household_number": 1}
        cls._population = cls.pop_factory.make_pop(cls.pop_params)
        cls._microcell = cls._population.cells[0].microcells[0]
        cls.person_susc = cls._microcell.persons[0]
        cls.person_susc.update_status(InfectionStatus(1))
        cls.person_symp = cls._microcell.persons[1]
        cls.person_symp.update_status(InfectionStatus(4))

        cls.interventionsweep.bind_population(cls._population)

    def test_bind_population(self):
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['case_isolation']), 9)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['vaccine_params']), 9)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['place_closure']), 2)
        self.assertEqual(len(pe.Parameters.instance().intervention_params[
                            'place_closure']), 9)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['household_quarantine']), 10)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['social_distancing']), 13)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['disease_testing']), 10)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['travel_isolation']), 10)
        self.assertEqual(len(
            self.interventionsweep.intervention_active_status.keys()), 8)

    def test___call__(self):
        self.interventionsweep(time=10)
        # Interventions are active, except the second place closure
        self.assertTrue(
            self.interventionsweep.intervention_active_status[
                [key for key in
                 self.interventionsweep.intervention_active_status.keys()
                 if isinstance(key, CaseIsolation)][0]])
        self.assertTrue(
            self.interventionsweep.intervention_active_status[
                [key for key in
                 self.interventionsweep.intervention_active_status.keys()
                 if isinstance(key, HouseholdQuarantine)][0]])
        self.assertTrue(
            self.interventionsweep.intervention_active_status[
                [key for key in
                 self.interventionsweep.intervention_active_status.keys()
                 if isinstance(key, PlaceClosure)][0]])
        self.assertFalse(
            self.interventionsweep.intervention_active_status[
                [key for key in
                 self.interventionsweep.intervention_active_status.keys()
                 if isinstance(key, PlaceClosure)][1]])
        self.assertTrue(
            self.interventionsweep.intervention_active_status[
                [key for key in
                 self.interventionsweep.intervention_active_status.keys()
                 if isinstance(key, SocialDistancing)][0]])
        self.assertTrue(
            self.interventionsweep.intervention_active_status[
                [key for key in
                 self.interventionsweep.intervention_active_status.keys()
                 if isinstance(key, DiseaseTesting)][0]])
        self.assertTrue(
            self.interventionsweep.intervention_active_status[
                [key for key in
                 self.interventionsweep.intervention_active_status.keys()
                 if isinstance(key, TravelIsolation)][0]])

        # Place is closed and social distancing ends
        self.assertIsNotNone(self.interventionsweep._population.cells[0].
                             microcells[0].closure_start_time)
        self.assertIsNotNone(self.interventionsweep._population.cells[0].
                             microcells[0].distancing_start_time)

        # Infector in case isolation, infectee in quarantine as
        # isolation_start_time = 100 as evaluated at this time (see above)
        self.interventionsweep.intervention_params['case_isolation'][
            'isolation_probability'] = 1.0
        self.interventionsweep.intervention_params['household_quarantine'][
            'quarantine_house_compliant'] = 1.0
        self.interventionsweep.intervention_params['household_quarantine'][
            'quarantine_individual_compliant'] = 1.0
        self.assertEqual(self.person_symp.isolation_start_time, 10)
        self.assertIsNotNone(self.person_susc.quarantine_start_time)

        # Stop isolating after start_time + policy_duration
        self.interventionsweep.intervention_params['case_isolation'][
            'policy_duration'] = 365
        self.person_symp.isolation_start_time = 370
        self.interventionsweep(time=370)
        self.assertEqual(self.person_symp.isolation_start_time, 370)
        self.interventionsweep(time=372)
        self.assertFalse(
            self.interventionsweep.intervention_active_status[
                [key for key in
                 self.interventionsweep.intervention_active_status.keys()
                 if isinstance(key, CaseIsolation)][0]])
        self.assertIsNone(self.person_symp.isolation_start_time)

        # The second place closure is active after its starting time
        self.interventionsweep(time=200)
        self.assertTrue(
            self.interventionsweep.intervention_active_status[
                [key for key in
                 self.interventionsweep.intervention_active_status.keys()
                 if isinstance(key, PlaceClosure)][1]])


if __name__ == '__main__':
    unittest.main()
