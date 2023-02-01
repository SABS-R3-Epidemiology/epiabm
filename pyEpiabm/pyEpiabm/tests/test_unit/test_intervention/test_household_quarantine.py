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
        cls.sympt_person = cls.test_population.cells[0].microcells[0].persons[0]
        cls.sympt_person.update_status(InfectionStatus.InfectMild)
        cls.susc_person = cls.test_population.cells[0].microcells[0].persons[1]
        cls.susc_person.update_status(InfectionStatus.Susceptible)

        cls.householdquarantine = \
            HouseholdQuarantine(start_time=6, policy_duration=365,
                                case_threshold=0, quarantine_delay=1,
                                quarantine_duration=14,
                                quarantine_house_compliant=1.0,
                                quarantine_individual_compliant=1.0,
                                quarantine_house_effectiveness=1.5,
                                quarantine_spatial_effectiveness=0.25,
                                quarantine_place_effectiveness=[
                                    0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                population=cls.test_population)

    def test__init__(self):
        self.assertEqual(self.householdquarantine.quarantine_duration, 14)
        self.assertEqual(self.householdquarantine.quarantine_delay, 1)
        self.assertEqual(self.householdquarantine.
                         quarantine_house_compliant, 1.0)
        self.assertEqual(self.householdquarantine.
                         quarantine_individual_compliant, 1.0)
        self.assertEqual(self.test_population.cells[0].
                         quarantine_house_effectiveness,
                         1.5)
        self.assertEqual(self.test_population.cells[0].
                         quarantine_spatial_effectiveness, 0.25)
        self.assertEqual(self.test_population.cells[0].
                         quarantine_place_effectiveness,
                         [0.25, 0.25, 0.25, 0.25, 0.25, 0.25])

    def test___call__(self):
        self.householdquarantine(time=3)
        self.assertIsNotNone(self.sympt_person.quarantine_start_time)
        self.assertIsNotNone(self.susc_person.quarantine_start_time)

        self.sympt_person.quarantine_start_time = 1
        self.householdquarantine(time=20)
        self.assertIsNone(self.sympt_person.quarantine_start_time)
        self.assertIsNone(self.susc_person.quarantine_start_time)

if __name__ == '__main__':
    unittest.main()
