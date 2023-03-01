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

        params = pe.Parameters.instance().intervention_params[
            'household_quarantine']
        params['quarantine_house_compliant'] = 1.0
        self.householdquarantine = HouseholdQuarantine(
            population=self.test_population, **params)

    def test__init__(self):
        self.assertEqual(self.householdquarantine.start_time, 6)
        self.assertEqual(self.householdquarantine.policy_duration, 365)
        self.assertEqual(self.householdquarantine.case_threshold, 0)
        self.assertEqual(self.householdquarantine.quarantine_duration, 14)
        self.assertEqual(self.householdquarantine.quarantine_delay, 1)
        self.assertEqual(self.householdquarantine.
                         quarantine_house_compliant, 1.0)
        self.assertEqual(self.householdquarantine.
                         quarantine_individual_compliant, 1.0)

    def test___call__(self):
        # Susceptible person in quarantine (100% compliant),
        # symptomatic in isolation (100% probability)
        self.householdquarantine.quarantine_house_compliant = 1.0
        self.householdquarantine.quarantine_individual_compliant = 1.0
        self.sympt_person.isolation_start_time = 3
        self.householdquarantine(time=3)
        self.assertIsNone(self.sympt_person.quarantine_start_time)
        self.assertEqual(self.susc_person1.quarantine_start_time, 4)

        # second household infection while in quarantine
        self.susc_person2.update_status(InfectionStatus.InfectMild)
        self.susc_person2.isolation_start_time = 6
        self.householdquarantine(time=6)
        self.assertIsNone(self.sympt_person.quarantine_start_time)
        self.assertEqual(self.susc_person1.quarantine_start_time, 7)

        # End quarantine
        self.householdquarantine(time=22)
        self.assertIsNone(self.sympt_person.quarantine_start_time)
        self.assertIsNone(self.susc_person1.quarantine_start_time)

    def test_turn_off(self):
        self.susc_person1.quarantine_start_time = 370
        self.householdquarantine(time=370)

        self.householdquarantine.turn_off()
        self.assertIsNone(self.susc_person1.quarantine_start_time)


if __name__ == '__main__':
    unittest.main()
