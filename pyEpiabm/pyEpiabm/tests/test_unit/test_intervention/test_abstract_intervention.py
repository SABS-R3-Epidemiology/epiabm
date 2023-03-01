import unittest

import pyEpiabm as pe
from pyEpiabm.intervention import AbstractIntervention


class TestAbstractIntervention(unittest.TestCase):
    """Test the 'AbstractIntervention' class.
    """

    def setUp(self) -> None:
        self.start_time = 1
        self.policy_duration = 10
        self.case_threshold = 20
        self._population = pe.Population()
        self.intervention_object = AbstractIntervention(self.start_time,
                                                        self.policy_duration,
                                                        self._population,
                                                        self.case_threshold)

    def test_construct(self):

        self.assertEqual(self.intervention_object.start_time, self.start_time)
        self.assertEqual(self.intervention_object.policy_duration,
                         self.policy_duration)
        self.assertEqual(self.intervention_object.case_threshold,
                         self.case_threshold)
        self.assertEqual(self.intervention_object._population,
                         self._population)

    def test_is_active(self):
        self.assertTrue(self.intervention_object.is_active(time=5,
                                                           num_cases=50))
        self.assertFalse(self.intervention_object.is_active(time=5,
                                                            num_cases=5))

    def test___call__(self):
        self.assertRaises(NotImplementedError,
                          self.intervention_object.__call__, 1)


if __name__ == '__main__':
    unittest.main()
