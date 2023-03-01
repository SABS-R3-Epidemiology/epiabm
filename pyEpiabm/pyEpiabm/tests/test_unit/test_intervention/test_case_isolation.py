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

        self.params = pe.Parameters.instance().intervention_params[
            'case_isolation']
        self.caseisolation = \
            CaseIsolation(population=self._population, **self.params)

    def test__init__(self):
        # Test the parameter values from params file (testing_parameters.json)
        self.assertEqual(self.caseisolation.start_time,
                         self.params['start_time'])
        self.assertEqual(self.caseisolation.policy_duration,
                         self.params['policy_duration'])
        self.assertEqual(self.caseisolation.case_threshold,
                         self.params['case_threshold'])
        self.assertEqual(self.caseisolation.isolation_delay,
                         self.params['isolation_delay'])
        self.assertEqual(self.caseisolation.isolation_duration,
                         self.params['isolation_duration'])
        self.assertEqual(self.caseisolation.isolation_probability,
                         self.params['isolation_probability'])

    def test___call__(self):
        # Before isolation starts
        self.assertFalse(hasattr(self.person_susc, 'isolation_start_time'))
        self.assertFalse(hasattr(self.person_symp, 'isolation_start_time'))

        # Start isolation if the person is symptomatic
        self.caseisolation.isolation_probability = 1.0
        self.caseisolation(time=5)
        self.assertFalse(hasattr(self.person_susc, 'isolation_start_time'))
        self.assertEqual(self.person_symp.isolation_start_time, 5)

        # End isolation
        self.caseisolation(time=150)
        self.assertFalse(hasattr(self.person_susc, 'isolation_start_time'))
        self.assertIsNone(self.person_symp.isolation_start_time)


if __name__ == '__main__':
    unittest.main()
