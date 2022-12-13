import unittest

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import CaseIsolation
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestCaseIsolation(TestPyEpiabm):
    """Test the 'CaseIsolation' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super(TestCaseIsolation, cls).setUpClass()  # Sets up patch on logging

        # construct a popultion with 5 persons
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._population.cells[0].microcells[0].add_people(5)
        for i in range(5):
            person = cls._population.cells[0].microcells[0].persons[i]
            person.update_status(InfectionStatus(i + 1))

        cls.caseisolation = CaseIsolation(start_time=6, policy_duration=365,
                                          threshold=0, isolation_duration=100,
                                          isolation_delay=0,
                                          isolation_probability=1,
                                          isolation_effectiveness=0,
                                          isolation_house_effectiveness=0,
                                          population=cls._population)

    def test__init__(self):
        self.assertEqual(self.caseisolation.isolation_duration, 100)
        self.assertEqual(self.caseisolation.isolation_delay, 0)
        self.assertEqual(self.caseisolation.isolation_probability, 1)
        self.assertEqual(self._population.cells[0].isolation_effectiveness, 0)
        self.assertEqual(self._population.cells[0].
                         isolation_house_effectiveness, 0)

    def test___call__(self):
        self.caseisolation(time=5)
        self.assertIsNone(self._population.cells[0].persons[0].
                          isolation_start_time)
        self._population.cells[0].persons[0].isolation_start_time = 1
        self.assertIsNotNone(self._population.cells[0].persons[0].
                             isolation_start_time)
        self.caseisolation(time=150)
        self.assertIsNone(self._population.cells[0].persons[0].
                          isolation_start_time)


if __name__ == '__main__':
    unittest.main()
