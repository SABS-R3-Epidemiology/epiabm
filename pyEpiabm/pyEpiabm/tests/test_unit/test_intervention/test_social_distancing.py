import unittest
from unittest.mock import patch

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import SocialDistancing
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestSocialDistancing(TestPyEpiabm):
    """Test the 'SocialDistancing' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Intialise a population with one cell and one microcell with
        one infector.
        """
        super(TestSocialDistancing, cls).setUpClass()  # Sets up parameters
        cls.time = 1
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 1, "cell_number": 1,
                          "microcell_number": 1, "household_number": 1}
        cls._population = cls.pop_factory.make_pop(cls.pop_params)
        cls.microcell = cls._population.cells[0].microcells[0]
        cls.person = cls.microcell.persons[0]
        cls.person.update_status(InfectionStatus(7))

        cls.params = pe.Parameters.instance().intervention_params[
            'social_distancing'][0]
        cls.socialdistancing = SocialDistancing(population=cls._population,
                                                **cls.params)

    def test__init__(self):
        # Test the parameter values from params file (testing_parameters.json)
        self.assertEqual(self.socialdistancing.start_time,
                         self.params['start_time'])
        self.assertEqual(self.socialdistancing.policy_duration,
                         self.params['policy_duration'])
        self.assertEqual(self.socialdistancing.case_threshold,
                         self.params['case_threshold'])
        self.assertEqual(self.socialdistancing.distancing_delay,
                         self.params['distancing_delay'])
        self.assertEqual(self.socialdistancing.distancing_duration,
                         self.params['distancing_duration'])
        self.assertEqual(self.socialdistancing.case_microcell_threshold,
                         self.params['case_microcell_threshold'])
        self.assertEqual(self.socialdistancing.distancing_enhanced_prob,
                         self.params['distancing_enhanced_prob'])

    def test___call__(self):
        # Social distancing haven't start
        self.assertFalse(hasattr(self.microcell, 'distancing_start_time'))
        # Age group exists with normal social distancing
        self.person.age_group = 0
        self.socialdistancing(time=5)
        self.assertTrue(hasattr(self.microcell, 'distancing_start_time'))
        self.assertFalse(self.person.distancing_enhanced)
        # Social distancing ends
        self.socialdistancing(time=150)
        self.assertIsNone(self.microcell.distancing_start_time)
        # Age group exists with enhanced social distancing
        self.person.age_group = 1
        self.socialdistancing(time=5)
        self.assertIsNotNone(self.microcell.distancing_start_time)
        self.assertTrue(self.person.distancing_enhanced)

    @patch('pyEpiabm.core.Parameters.instance')
    def test___call__no_age(self, mock_params):
        self.microcell.distancing_start_time = None
        # Age group not exists
        mock_params.return_value.use_ages = False
        self.socialdistancing(time=5)
        self.assertFalse(self.person.distancing_enhanced)

    def test_turn_off(self):
        self.microcell.distancing_start_time = 370
        self.socialdistancing.turn_off()
        self.assertIsNone(self.microcell.distancing_start_time)


if __name__ == '__main__':
    unittest.main()
