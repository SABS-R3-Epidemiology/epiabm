import unittest

import pyEpiabm as pe
from pyEpiabm.intervention import AbstractIntervention


class TestAbstractIntervention(unittest.TestCase):
    """Test the 'AbstractIntervention' class.
    """

    def test_construct(self):
        start_time = 1
        policy_duration = 10
        case_threshold = 20
        population = pe.Population()
        intervention_object = AbstractIntervention(start_time, policy_duration,
                                                   case_threshold, population)
        self.assertEqual(intervention_object.start_time, 1)
        self.assertEqual(intervention_object.policy_duration, 10)
        self.assertEqual(intervention_object.case_threshold, 20)
        self.assertEqual(intervention_object._population, population)

    def test_is_active(self):
        intervention_object = AbstractIntervention(start_time=1,
                                                   policy_duration=10,
                                                   case_threshold=20,
                                                   population=pe.Population())
        self.assertTrue(intervention_object.is_active(time=5, num_cases=50))
        intervention_object = AbstractIntervention(start_time=1,
                                                   policy_duration=10,
                                                   case_threshold=20,
                                                   population=pe.Population())
        self.assertFalse(intervention_object.is_active(time=5, num_cases=5))

    def test___call__(self):
        intervention_object = AbstractIntervention(start_time=1,
                                                   policy_duration=10,
                                                   case_threshold=20,
                                                   population=pe.Population())
        self.assertRaises(NotImplementedError, intervention_object.__call__, 1)


if __name__ == '__main__':
    unittest.main()
