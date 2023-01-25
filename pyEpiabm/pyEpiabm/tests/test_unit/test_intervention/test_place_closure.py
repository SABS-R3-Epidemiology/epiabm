import unittest

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import PlaceClosure
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestCaseIsolation(TestPyEpiabm):
    """Test the 'CaseIsolation' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        super(TestCaseIsolation, cls).setUpClass()  # Sets up parameters
        cls.time = 1
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._population.cells[0].microcells[0].add_people(2)
        for person in cls._population.cells[0].microcells[0].persons:
            person.update_status(InfectionStatus(7))

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

    def test__init__(self):
        self.assertEqual(self.placeclosure.closure_delay, 0)
        self.assertEqual(self.placeclosure.closure_duration, 100)
        self.assertEqual(self.placeclosure.icu_microcell_threshold, 1)
        self.assertEqual(self.placeclosure.case_microcell_threshold, 1)
        self.assertEqual(self._population.cells[0].microcells[0].
                         closure_household_infectiousness, 5)
        self.assertEqual(self._population.cells[0].microcells[0].
                         closure_spatial_params, 0.5)

    def test___call__(self):
        self.assertIsNone(self._population.cells[0].microcells[0].
                          closure_start_time)
        self.placeclosure(time=5)
        self.assertIsNotNone(self._population.cells[0].microcells[0].
                             closure_start_time)
        self.placeclosure(time=150)
        self.assertIsNone(self._population.cells[0].microcells[0].
                          closure_start_time)


if __name__ == '__main__':
    unittest.main()
