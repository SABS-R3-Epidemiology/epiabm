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

        # Construct a population with 2 persons
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._population.cells[0].microcells[0].add_people(2)
        cls.person_susc = cls._population.cells[0].microcells[0].persons[0]
        cls.person_susc.update_status(InfectionStatus(1))
        cls.person_symp = cls._population.cells[0].microcells[0].persons[1]
        cls.person_symp.update_status(InfectionStatus(4))

        params = pe.Parameters.instance().intervention_params['case_isolation']
        cls.caseisolation = CaseIsolation(population=cls._population, **params)

    def test__init__(self):
        self.assertEqual(self.caseisolation.start_time, 6)
        self.assertEqual(self.caseisolation.policy_duration, 365)
        self.assertEqual(self.caseisolation.case_threshold, 0)
        self.assertEqual(self.caseisolation.isolation_delay, 0)
        self.assertEqual(self.caseisolation.isolation_duration, 100)
        self.assertEqual(self.caseisolation.isolation_probability, 1)

    def test___call__(self):
        # Before isolation starts
        self.assertIsNone(self.person_susc.isolation_start_time)
        self.assertIsNone(self.person_symp.isolation_start_time)

        # Start isolation if the person is symptomatic
        self.caseisolation(time=5)
        self.assertIsNone(self.person_susc.isolation_start_time)
        self.assertEqual(self.person_symp.isolation_start_time, 5)

        # End isolation
        self.caseisolation(time=150)
        self.assertIsNone(self.person_susc.isolation_start_time)
        self.assertIsNone(self.person_symp.isolation_start_time)

    def test_turn_off(self):
        self.person_symp.isolation_start_time = 370
        self.caseisolation.turn_off()
        self.assertIsNone(self.person_symp.isolation_start_time)


if __name__ == '__main__':
    unittest.main()
