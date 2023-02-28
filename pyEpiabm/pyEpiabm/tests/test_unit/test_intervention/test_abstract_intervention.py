import unittest

import pyEpiabm as pe
from pyEpiabm.intervention import AbstractIntervention


class TestAbstractIntervention(unittest.TestCase):
    """Test the 'AbstractIntervention' class.

    """

    @classmethod
    def setUpClass(cls) -> None:
        super(TestAbstractIntervention, cls).setUpClass()

        cls.population = pe.Population()
        cls.intervention_object = AbstractIntervention(
            start_time=1,
            policy_duration=10,
            case_threshold=20,
            population=cls.population)

    def test_construct(self):
        self.assertEqual(self.intervention_object.start_time, 1)
        self.assertEqual(self.intervention_object.policy_duration, 10)
        self.assertEqual(self.intervention_object.case_threshold, 20)
        self.assertEqual(self.intervention_object._population, self.population)

    def test_is_active(self):
        self.assertTrue(self.intervention_object.is_active(time=5,
                                                           num_cases=50))
        self.assertFalse(self.intervention_object.is_active(time=5,
                                                            num_cases=5))
        self.assertFalse(self.intervention_object.is_active(time=0,
                                                            num_cases=50))

    def test___call__(self):
        self.assertRaises(NotImplementedError,
                          self.intervention_object.__call__, 1)

    def test_turn_off(self):
        self.assertRaises(NotImplementedError,
                          self.intervention_object.turn_off)


if __name__ == '__main__':
    unittest.main()
