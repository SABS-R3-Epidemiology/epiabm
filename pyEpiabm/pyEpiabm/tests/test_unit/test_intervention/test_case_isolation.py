import unittest

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import CaseIsolation
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestCaseIsolation(TestPyEpiabm):
    """Test the 'CaseIsolation' class.
    """

    def setUp(self) -> None:
        super(TestCaseIsolation, self).setUp()  # Sets up patch on logging

        # Construct a population with 2 persons
        self.pop_factory = pe.routine.ToyPopulationFactory()
        self.pop_params = {"population_size": 2, "cell_number": 1,
                           "microcell_number": 1, "household_number": 1}
        self._population = self.pop_factory.make_pop(self.pop_params)
        self.person_susc = self._population.cells[0].microcells[0].persons[0]
        self.person_susc.update_status(InfectionStatus(1))
        self.person_symp = self._population.cells[0].microcells[0].persons[1]
        self.person_symp.update_status(InfectionStatus(4))

        params = pe.Parameters.instance().intervention_params['case_isolation']
        self.caseisolation = \
            CaseIsolation(population=self._population, **params)

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
        self.caseisolation.isolation_probability = 1.0
        self.caseisolation(time=5)
        self.assertIsNone(self.person_susc.isolation_start_time)
        self.assertEqual(self.person_symp.isolation_start_time, 5)

        # End isolation
        self.caseisolation(time=150)
        self.assertIsNone(self.person_susc.isolation_start_time)
        self.assertIsNone(self.person_symp.isolation_start_time)

    def test_turn_off(self):
        self.person_symp.isolation_start_time = 370
        self.caseisolation(time=370)

        self.caseisolation.turn_off()
        self.assertIsNone(self.person_symp.isolation_start_time)


if __name__ == '__main__':
    unittest.main()
