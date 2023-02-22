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
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
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

        params = pe.Parameters.instance().intervention_params[
            'social_distancing']
        cls.socialdistancing = SocialDistancing(population=cls._population,
                                                **params)

    def test__init__(self):
        self.assertEqual(self.socialdistancing.start_time, 6)
        self.assertEqual(self.socialdistancing.policy_duration, 365)
        self.assertEqual(self.socialdistancing.case_threshold, 0)
        self.assertEqual(self.socialdistancing.distancing_delay, 0)
        self.assertEqual(self.socialdistancing.distancing_duration, 100)
        self.assertEqual(self.socialdistancing.distancing_compliant, 1)
        self.assertEqual(self.socialdistancing.case_microcell_threshold, 1)
        self.assertEqual(self.socialdistancing.distancing_enhanced_prob,
                         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    def test___call__(self):
        # Social distancing haven't start
        self.assertIsNone(self.microcell.distancing_start_time)
        # Age group exists with normal social distancing
        self.person.age_group = 0
        self.socialdistancing(time=5)
        self.assertIsNotNone(self.microcell.distancing_start_time)
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


if __name__ == '__main__':
    unittest.main()
