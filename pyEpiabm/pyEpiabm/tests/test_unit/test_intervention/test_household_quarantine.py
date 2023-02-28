import unittest

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import HouseholdQuarantine
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestHouseholdQuarantine(TestPyEpiabm):
    """Test the 'HouseholdQuarantine' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super(TestHouseholdQuarantine, cls).setUpClass()

        # Construct a population with 2 persons in 1 household.
        # One symptomatic the other susceptible
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 2, "cell_number": 1,
                          "microcell_number": 1, "household_number": 1}
        cls.test_population = cls.pop_factory.make_pop(cls.pop_params)
        cls.sympt_person = cls.test_population.cells[0].microcells[
            0].persons[0]
        cls.sympt_person.update_status(InfectionStatus.InfectMild)
        cls.susc_person = cls.test_population.cells[0].microcells[0].persons[1]
        cls.susc_person.update_status(InfectionStatus.Susceptible)

        params = pe.Parameters.instance().intervention_params[
            'household_quarantine']
        params['quarantine_house_compliant'] = 1.0
        cls.householdquarantine = HouseholdQuarantine(
            population=cls.test_population, **params)

    def test__init__(self):
        # Test the parameter values from params file (testing_parameters.json)
        params = pe.Parameters.instance().intervention_params[
                'household_quarantine']
        self.assertEqual(self.householdquarantine.start_time,
                         params['start_time'])
        self.assertEqual(self.householdquarantine.policy_duration,
                         params['policy_duration'])
        self.assertEqual(self.householdquarantine.case_threshold,
                         params['case_threshold'])
        self.assertEqual(self.householdquarantine.quarantine_duration,
                         params['quarantine_duration'])
        self.assertEqual(self.householdquarantine.quarantine_delay,
                         params['quarantine_delay'])
        self.assertEqual(self.householdquarantine.
                         quarantine_house_compliant,
                         params['quarantine_house_compliant'])
        self.assertEqual(self.householdquarantine.
                         quarantine_individual_compliant,
                         params['quarantine_individual_compliant'])

    def test___call__(self):
        # Both in quarantine as one symptomatic and 100% compliance
        self.householdquarantine(time=3)
        self.assertIsNotNone(self.sympt_person.quarantine_start_time)
        self.assertIsNotNone(self.susc_person.quarantine_start_time)

        # End quarantine
        self.sympt_person.quarantine_start_time = 1
        self.householdquarantine(time=20)
        self.assertIsNone(self.sympt_person.quarantine_start_time)
        self.assertIsNone(self.susc_person.quarantine_start_time)


if __name__ == '__main__':
    unittest.main()
