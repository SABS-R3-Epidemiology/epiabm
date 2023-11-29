import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import TravelIsolation
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestTravelIsolation(TestPyEpiabm):
    """Test the 'TravelIsolation' class.
    """

    def setUp(self) -> None:
        super(TestTravelIsolation, self).setUp()  # Sets up patch on logging

        # Construct a population with 2 persons
        self.pop_factory = pe.routine.ToyPopulationFactory()
        self.pop_params = {"population_size": 2, "cell_number": 1,
                           "microcell_number": 1, "household_number": 1}
        self._population = self.pop_factory.make_pop(self.pop_params)
        self._microcell = self._population.cells[0].microcells[0]
        self.person_susc = self._population.cells[0].microcells[0].persons[0]
        self.person_susc.update_status(InfectionStatus.Susceptible)
        self.person_symp = self._population.cells[0].microcells[0].persons[1]
        self.person_symp.update_status(InfectionStatus.InfectMild)

        # Introduce travelling individual
        self._microcell.add_people(
            1, status=InfectionStatus.InfectASympt, age_group=5)
        self.person_introduced = self._microcell.persons[2]
        self._population.travellers.append(self.person_introduced)
        self._microcell.households[0].add_person(self.person_introduced)
        self.person_introduced.travel_end_time = 25

        self.params = pe.Parameters.instance().intervention_params[
            'travel_isolation']
        self.travelisolation = \
            TravelIsolation(population=self._population, **self.params)

    def test__init__(self):
        # Test the parameter values from params file (testing_parameters.json)
        self.assertEqual(self.travelisolation.start_time,
                         self.params['start_time'])
        self.assertEqual(self.travelisolation.policy_duration,
                         self.params['policy_duration'])
        self.assertEqual(self.travelisolation.case_threshold,
                         self.params['case_threshold'])
        self.assertEqual(self.travelisolation.isolation_delay,
                         self.params['isolation_delay'])
        self.assertEqual(self.travelisolation.isolation_duration,
                         self.params['isolation_duration'])
        self.assertEqual(self.travelisolation.isolation_probability,
                         self.params['isolation_probability'])
        self.assertEqual(self.travelisolation.use_testing,
                         self.params['use_testing'])
        self.assertEqual(self.travelisolation.hotel_isolate,
                         self.params['hotel_isolate'])

    @mock.patch('random.random')
    def test___call__(self, mock_random):
        mock_random.return_value = 0
        # Before travel isolation starts
        self.assertFalse(hasattr(
            self.person_introduced, 'travel_isolation_start_time'))

        # Create individual and test re-assigning household
        self.assertEqual(len(self._microcell.households), 1)
        self.assertEqual(len(self.person_symp.household.persons), 3)
        self.travelisolation(time=11)
        self.assertEqual(len(self._microcell.households), 2)
        self.assertEqual(len(self.person_symp.household.persons), 2)
        self.assertEqual(len(self.person_introduced.household.persons), 1)

        # Out of travel_isolation (after 5 days) assign back to household
        self.travelisolation(time=20)
        self.assertIsNone(self.person_introduced.travel_isolation_start_time)
        self.assertEqual(len(self._microcell.households), 1)
        self.assertEqual(len(self.person_symp.household.persons), 3)

        # Introduce individual in single household
        self._microcell.add_people(
            1, status=InfectionStatus.InfectASympt, age_group=7)
        person_introduced2 = self._microcell.persons[3]
        self._population.travellers.append(person_introduced2)
        self._microcell.add_household([person_introduced2], change_id=False)
        person_introduced2.travel_end_time = 40
        self.travelisolation(time=21)
        self.assertTrue(person_introduced2.household.isolation_location)
        mock_random.return_value = 1
        self.travelisolation(time=28)
        self.assertFalse(person_introduced2.household.isolation_location)

    @mock.patch('random.random')
    def test_person_selection(self, mock_random):
        mock_random.return_value = 0
        self.travelisolation.use_testing = 1
        self.person_introduced.date_positive = 0
        self.travelisolation(time=1)

        self.assertTrue(self.travelisolation.
                        person_selection_method(self.person_introduced))
        self.assertEqual(self.person_introduced.travel_isolation_start_time, 1)

    def test_turn_off(self):
        self.person_introduced.travel_isolation_start_time = 370
        self.travelisolation(time=370)
        self.travelisolation.turn_off()
        self.assertIsNone(self.person_introduced.travel_isolation_start_time)


if __name__ == '__main__':
    unittest.main()
