import unittest

import pyEpiabm as pe
from pyEpiabm.property import HouseholdInfection
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
            person.infectiousness = 1.0
        cls.infector = cls._population.cells[0].microcells[0].persons[0]
        cls.infectee = cls._population.cells[0].microcells[0].persons[1]

    def test_house_inf(self):
        result = HouseholdInfection.household_inf(self.infector, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_susc(self):
        result = HouseholdInfection.household_susc(
            self.infector, self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_inf_force(self):
        result = HouseholdInfection.household_foi(
            self.infector, self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_case_isolation(self):
        result = HouseholdInfection.household_foi(
            self.infector, self.infectee, self.time)
        # Case isolate
        isolation_house_effectiveness = 0.5
        self._population.cells[0].\
            isolation_house_effectiveness = isolation_house_effectiveness
        self.infector.isolation_start_time = 1
        result_isolating = HouseholdInfection.household_foi(self.infector,
                                                            self.infectee,
                                                            self.time)
        self.assertEqual(result*isolation_house_effectiveness,
                         result_isolating)

    def test_house_place_closure(self):
        result = HouseholdInfection.household_inf(
            self.infector, self.time)
        # Place closure
        closure_household_infectiousness = 0.5
        self._population.cells[0].microcells[0].\
            closure_household_infectiousness = closure_household_infectiousness
        self.infector.microcell.closure_start_time = 1
        result_closure = HouseholdInfection.household_inf(
            self.infector, self.time)
        self.assertEqual(result*closure_household_infectiousness,
                         result_closure)


if __name__ == '__main__':
    unittest.main()
