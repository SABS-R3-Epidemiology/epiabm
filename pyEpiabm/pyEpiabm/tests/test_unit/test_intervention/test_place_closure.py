import unittest

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.intervention import PlaceClosure
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestPlaceClosure(TestPyEpiabm):
    """Test the 'PlaceClosure' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        super(TestPlaceClosure, cls).setUpClass()  # Sets up parameters
        cls.time = 1
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 2, "cell_number": 1,
                          "microcell_number": 1, "household_number": 1}
        cls._population = cls.pop_factory.make_pop(cls.pop_params)
        cls.microcell = cls._population.cells[0].microcells[0]
        for person in cls._population.cells[0].microcells[0].persons:
            person.update_status(InfectionStatus(7))

        params = pe.Parameters.instance().intervention_params['place_closure']
        cls.placeclosure = PlaceClosure(population=cls._population, **params)

    def test__init__(self):
        # Test the parameter values from params file (testing_parameters.json)
        params = pe.Parameters.instance().intervention_params[
                'place_closure']
        self.assertEqual(self.placeclosure.start_time,
                         params['start_time'])
        self.assertEqual(self.placeclosure.policy_duration,
                         params['policy_duration'])
        self.assertEqual(self.placeclosure.case_threshold,
                         params['case_threshold'])
        self.assertEqual(self.placeclosure.closure_delay,
                         params['closure_delay'])
        self.assertEqual(self.placeclosure.closure_duration,
                         params['closure_duration'])
        self.assertEqual(self.placeclosure.case_microcell_threshold,
                         params['case_microcell_threshold'])

    def test___call__(self):
        self.assertFalse(hasattr(self.microcell, 'closure_start_time'))
        self.placeclosure(time=5)
        self.assertIsNotNone(self.microcell.closure_start_time)
        self.placeclosure(time=150)
        self.assertIsNone(self.microcell.closure_start_time)


if __name__ == '__main__':
    unittest.main()
