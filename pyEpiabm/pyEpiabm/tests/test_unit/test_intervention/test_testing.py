import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import DiseaseTesting
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestDiseaseTesting(TestPyEpiabm):
    """Test the 'DiseaseTesting' class.

    """
    def setUp(self) -> None:
        super(TestDiseaseTesting, self).setUp()  # Sets up patch on logging

        # Construct a population with 2 persons
        self.pop_factory = pe.routine.ToyPopulationFactory()
        self.pop_params = {"population_size": 2, "cell_number": 1,
                           "microcell_number": 1, "household_number": 1}
        self._population = self.pop_factory.make_pop(self.pop_params)
        self.cell = self._population.cells[0]
        self.person1 = self._population.cells[0].microcells[0].persons[0]
        self.person2 = self._population.cells[0].microcells[0].persons[1]

        self.params = pe.Parameters.instance().intervention_params[
            'testing']
        self.testing = \
            DiseaseTesting(population=self._population, **self.params)

    def test__init__(self):
        # Test the parameter values from params file (testing_parameters.json)
        self.assertEqual(self.testing.start_time,
                         self.params['start_time'])
        self.assertEqual(self.testing.policy_duration,
                         self.params['policy_duration'])
        self.assertEqual(self.testing.case_threshold,
                         self.params['case_threshold'])
        self.assertEqual(self.testing.testing_capacity,
                         self.params['testing_capacity'])
        self.assertEqual(self.testing.false_negative,
                         self.params['false_negative'])
        self.assertEqual(self.testing.false_positive,
                         self.params['false_positive'])

    @mock.patch('random.random')
    def test_true_results(self, mock_random):
        mock_random.return_value = 1
        self.person1.infection_status = InfectionStatus.InfectMild
        self.person2.infection_status = InfectionStatus.InfectMild
        self.cell.enqueue_PCR_testing(self.person1)
        self.cell.enqueue_LFT_testing(self.person2)

        self.testing(time=1.0)

        self.assertEqual(self.cell.PCR_queue.qsize(), 0)
        self.assertEqual(self.cell.LFT_queue.qsize(), 0)
        self.assertEqual(self.person1.date_positive, 1.0)
        self.assertEqual(self.person2.date_positive, 1.0)
        self.assertEqual(self._population.test_count[0], 2)

        self.assertEqual(mock_random.call_count, 2)

    @mock.patch('random.random')
    def test_false_results(self, mock_random):
        mock_random.return_value = 0
        self.person1.infection_status = InfectionStatus.Susceptible
        self.person2.infection_status = InfectionStatus.Susceptible

        self.cell.enqueue_PCR_testing(self.person1)
        self.cell.enqueue_LFT_testing(self.person2)

        self.testing(time=1.0)

        self.assertEqual(self.cell.PCR_queue.qsize(), 0)
        self.assertEqual(self.cell.LFT_queue.qsize(), 0)
        self.assertEqual(self.person1.date_positive, 1.0)
        self.assertEqual(self.person2.date_positive, 1.0)
        self.assertEqual(self._population.test_count[1], 2)

        self.assertEqual(mock_random.call_count, 2)

    def test_turn_off(self):
        self.person1.date_positive = 1.0
        self.person2.date_positive = 1.0

        self.testing.turn_off()

        self.assertIsNone(self.person1.date_positive)
        self.assertIsNone(self.person2.date_positive)


if __name__ == '__main__':
    unittest.main()
