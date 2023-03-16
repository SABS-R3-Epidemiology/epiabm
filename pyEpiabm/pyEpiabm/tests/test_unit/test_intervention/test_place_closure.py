import unittest

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import PlaceClosure
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestPlaceClosure(TestPyEpiabm):
    """Test the 'PlaceClosure' class.
    """

    def setUp(self) -> None:
        """Intialise a population with one cell and one microcell with
        one infector.
        """
        super(TestPlaceClosure, self).setUp()  # Sets up parameters

        self.time = 1
        self.pop_factory = pe.routine.ToyPopulationFactory()
        self.pop_params = {"population_size": 1, "cell_number": 1,
                           "microcell_number": 1}
        self._population = self.pop_factory.make_pop(self.pop_params)
        self._microcell = self._population.cells[0].microcells[0]
        self._microcell.persons[0].update_status(InfectionStatus(7))

        self.params = pe.Parameters.instance().intervention_params[
            'place_closure'][0]
        self.placeclosure = PlaceClosure(population=self._population,
                                         **self.params)

    def test__init__(self):
        # Test the parameter values from params file (testing_parameters.json)
        self.assertEqual(self.placeclosure.start_time,
                         self.params['start_time'])
        self.assertEqual(self.placeclosure.policy_duration,
                         self.params['policy_duration'])
        self.assertEqual(self.placeclosure.case_threshold,
                         self.params['case_threshold'])
        self.assertEqual(self.placeclosure.closure_delay,
                         self.params['closure_delay'])
        self.assertEqual(self.placeclosure.closure_duration,
                         self.params['closure_duration'])
        self.assertEqual(self.placeclosure.case_microcell_threshold,
                         self.params['case_microcell_threshold'])

    def test___call__(self):
        self.assertFalse(hasattr(self._microcell, 'closure_start_time'))
        self.placeclosure(time=5)
        self.assertIsNotNone(self._microcell.closure_start_time)
        self.placeclosure(time=150)
        self.assertIsNone(self._microcell.closure_start_time)

    def test_turn_off(self):
        self._microcell.closure_start_time = 370
        self.placeclosure(time=370)

        self.placeclosure.turn_off()
        self.assertIsNone(self._microcell.closure_start_time)


if __name__ == '__main__':
    unittest.main()
