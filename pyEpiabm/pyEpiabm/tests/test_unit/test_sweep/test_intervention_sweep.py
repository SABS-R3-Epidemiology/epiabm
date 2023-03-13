import unittest

import pyEpiabm as pe
from pyEpiabm.core import Parameters
from pyEpiabm.sweep import InterventionSweep
from pyEpiabm.property import InfectionStatus
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm
from pyEpiabm.intervention import CaseIsolation, HouseholdQuarantine, \
    PlaceClosure, SocialDistancing, DiseaseTesting, TravelIsolation


class TestInterventionSweep(TestPyEpiabm):
    """Test the 'InterventionSweep' class.
    """

    def setUp(self) -> None:
        super(TestInterventionSweep, self).setUp()
        self.interventionsweep = InterventionSweep()

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

        self.interventionsweep.bind_population(self._population)

    def test_bind_population(self):
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['case_isolation']), 9)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['vaccine_params']), 9)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['place_closure']), 9)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['household_quarantine']), 10)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['social_distancing']), 13)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['disease_testing']), 10)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['travel_isolation']), 10)
        self.assertEqual(len(
            self.interventionsweep.intervention_active_status.keys()), 7)

    def test___call__(self):
        self.interventionsweep(time=10)
        # Interventions are active
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

        # Create individual and test re-assigning household
        self._microcell.add_people(
            1, status=InfectionStatus.InfectASympt, age_group=5)
        person_introduced = self._microcell.persons[2]
        self._microcell.households[0].add_person(person_introduced)
        person_introduced.travel_end_time = 25
        # pe.Parameters.instance().intervention_params['travel_isolation'][
        #     'hotel_isolate'] = 1
        # pe.Parameters.instance().intervention_params['travel_isolation'][
        #     'isolation_probability'] = 1.0
        # Why parameters not set?
        self.assertEqual(len(self._microcell.households), 1)
        self.assertEqual(len(self.person_symp.household.persons), 3)
        self.interventionsweep(time=11)
        self.assertEqual(len(self._microcell.households), 2)
        self.assertEqual(len(self.person_symp.household.persons), 2)
        self.assertEqual(len(person_introduced.household.persons), 1)

        # Out of travel_isolation assign back to household
        pe.Parameters.instance().travel_params['prob_existing_household'] = 1.0
        self.interventionsweep(time=20)
        self.assertIsNone(person_introduced.travel_isolation_start_time)
        self.assertEqual(len(self._microcell.households), 1)
        self.assertEqual(len(self.person_symp.household.persons), 3)

        # Stop isolating after start_time + policy_duration
        self.interventionsweep.intervention_params['case_isolation'][
            'policy_duration'] = 365
        # possibly doesnt work
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


if __name__ == '__main__':
    unittest.main()
