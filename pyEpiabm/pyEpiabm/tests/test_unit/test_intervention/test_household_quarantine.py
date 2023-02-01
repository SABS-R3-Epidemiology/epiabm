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

        # Construct a population with 5 persons
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._population.cells[0].microcells[0].add_people(5)
        for i in range(5):
            person = cls._population.cells[0].microcells[0].persons[i]
            person.update_status(InfectionStatus(i + 1))

        cls.householdquarantine = \
            HouseholdQuarantine(time_start=6, policy_duration=365,
                                case_threshold=0, quarantine_delay=1,
                                quarantine_duration=14,
                                quarantine_house_compliant=0.75,
                                quarantine_individual_compliant=1.0,
                                quarantine_house_effectiveness=1.5,
                                quarantine_spatial_effectiveness=0.25,
                                quarantine_place_effectiveness=[
                                    0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                population=cls._population)

    def test__init__(self):
        self.assertEqual(self.householdquarantine.quarantine_duration, 14)
        self.assertEqual(self.householdquarantine.quarantine_delay, 1)
        self.assertEqual(self.householdquarantine.
                         quarantine_house_compliant, 0.75)
        self.assertEqual(self.householdquarantine.
                         quarantine_individual_compliant, 1.0)
        self.assertEqual(self._population.cells[0].
                         quarantine_house_effectiveness,
                         1.5)
        self.assertEqual(self._population.cells[0].
                         quarantine_spatial_effectiveness, 0.25)
        self.assertEqual(self._population.cells[0].
                         quarantine_place_effectiveness,
                         [0.25, 0.25, 0.25, 0.25, 0.25, 0.25])

    def test___call__(self):
        self.householdquarantine(time=5)
        self.assertIsNone(self._population.cells[0].persons[0].
                          quarantine_start_time)
        self._population.cells[0].persons[0].quarantine_start_time = 1
        self.assertIsNotNone(self._population.cells[0].persons[0].
                             quarantine_start_time)
        self.householdquarantine(time=16)
        self.assertIsNone(self._population.cells[0].persons[0].
                          quarantine_start_time)


if __name__ == '__main__':
    unittest.main()
