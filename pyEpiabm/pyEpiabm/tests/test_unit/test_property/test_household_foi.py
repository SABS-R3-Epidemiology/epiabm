import unittest

import pyEpiabm as pe
from pyEpiabm.property import HouseholdInfection, InfectionStatus
from pyEpiabm.intervention import PlaceClosure
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestHouseholdInfection(TestPyEpiabm):
    """Test the 'HouseholdInfection' class, which contains the
    infectiousness and susceptibility calculations that
    determine whether infection events occur within households.
    Each function should return a number greater than 0.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        super(TestHouseholdInfection, cls).setUpClass()  # Sets up parameters
        cls.time = 1
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._population.cells[0].microcells[0].add_people(2)
        for person in cls._population.cells[0].microcells[0].persons:
            person.update_status(InfectionStatus(7))
            person.infectiousness = 1.0
        cls.placeclosure = PlaceClosure(start_time=1,
                                        policy_duration=365,
                                        case_threshold=0,
                                        closure_delay=0,
                                        closure_duration=100,
                                        closure_household_infectiousness=5,
                                        closure_spatial_params=0.5,
                                        icu_microcell_threshold=1,
                                        case_microcell_threshold=1,
                                        population=cls._population)

    def test_house_inf(self):
        self.placeclosure(self.time)
        result = HouseholdInfection.household_inf(self._population.cells[0].
                                                  microcells[0].persons[0],
                                                  self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_susc(self):
        result = HouseholdInfection.household_susc(
            self._population.cells[0].microcells[0].persons[0],
            self._population.cells[0].microcells[0].persons[1],
            self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_inf_force(self):
        result = HouseholdInfection.household_foi(
            self._population.cells[0].microcells[0].persons[0],
            self._population.cells[0].microcells[0].persons[1],
            self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_case_isolation(self):
        infector = self._population.cells[0].microcells[0].persons[0]
        infectee = self._population.cells[0].microcells[0].persons[1]
        result = HouseholdInfection.household_foi(
            infector, infectee, self.time)
        # Case isolate
        isolation_house_effectiveness = 0.5
        self._population.cells[0].\
            isolation_house_effectiveness = isolation_house_effectiveness
        infector.isolation_start_time = 1
        result_isolating = HouseholdInfection.household_foi(infector, infectee,
                                                            self.time)
        self.assertEqual(result*isolation_house_effectiveness,
                         result_isolating)


if __name__ == '__main__':
    unittest.main()
