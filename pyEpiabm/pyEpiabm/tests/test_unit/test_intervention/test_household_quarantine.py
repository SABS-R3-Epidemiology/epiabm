import unittest

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import HouseholdQuarantine
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestHouseholdQuarantine(TestPyEpiabm):
    """Test the 'HouseholdQuarantine' class.
    """

    def setUp(self) -> None:
        super(TestHouseholdQuarantine, self).setUp()

        # Construct a population with 3 persons in 1 household.
        # One symptomatic and two susceptible.
        self.pop_factory = pe.routine.ToyPopulationFactory()
        self.pop_params = {"population_size": 3, "cell_number": 1,
                           "microcell_number": 1, "household_number": 1}
        self.test_population = self.pop_factory.make_pop(self.pop_params)
        self.sympt_person = self.test_population.cells[0].microcells[
            0].persons[0]
        self.sympt_person.update_status(InfectionStatus.InfectMild)
        self.susc_person1 = \
            self.test_population.cells[0].microcells[0].persons[1]
        self.susc_person1.update_status(InfectionStatus.Susceptible)
        self.susc_person2 = \
            self.test_population.cells[0].microcells[0].persons[2]
        self.susc_person2.update_status(InfectionStatus.Susceptible)

        self.params = pe.Parameters.instance().intervention_params[
            'household_quarantine'][0]
        self.params['quarantine_house_compliant'] = 1.0
        self.householdquarantine = HouseholdQuarantine(
            population=self.test_population, **self.params)

    def test__init__(self):
        # Test the parameter values from params file (testing_parameters.json)
        self.assertEqual(self.householdquarantine.start_time,
                         self.params['start_time'])
        self.assertEqual(self.householdquarantine.policy_duration,
                         self.params['policy_duration'])
        self.assertEqual(self.householdquarantine.case_threshold,
                         self.params['case_threshold'])
        self.assertEqual(self.householdquarantine.quarantine_duration,
                         self.params['quarantine_duration'])
        self.assertEqual(self.householdquarantine.quarantine_delay,
                         self.params['quarantine_delay'])
        self.assertEqual(self.householdquarantine.
                         quarantine_house_compliant,
                         self.params['quarantine_house_compliant'])
        self.assertEqual(self.householdquarantine.
                         quarantine_individual_compliant,
                         self.params['quarantine_individual_compliant'])

    def test___call__(self):
        # Susceptible person in quarantine (100% compliant),
        # symptomatic in isolation (100% probability)
        self.householdquarantine.quarantine_house_compliant = 1.0
        self.householdquarantine.quarantine_individual_compliant = 1.0
        self.sympt_person.isolation_start_time = 3
        self.householdquarantine(time=3)
        self.assertFalse(hasattr(self.sympt_person, 'quarantine_start_time'))
        self.assertEqual(self.susc_person1.quarantine_start_time, 4)
        self.assertEqual(self.susc_person2.quarantine_start_time, 4)

        # Second household infection while in quarantine. Quarantine
        # also assigned to first infected individual still in isolation.
        self.susc_person2.isolation_start_time = 6
        self.householdquarantine(time=6)
        self.assertEqual(self.sympt_person.quarantine_start_time, 7)
        self.assertEqual(self.susc_person1.quarantine_start_time, 7)

        # End quarantine
        self.householdquarantine(time=22)
        self.assertIsNone(self.susc_person1.quarantine_start_time)

    def test_turn_off(self):
        self.susc_person1.quarantine_start_time = 370
        self.householdquarantine(time=370)

        self.householdquarantine.turn_off()
        self.assertIsNone(self.susc_person1.quarantine_start_time)


if __name__ == '__main__':
    unittest.main()
