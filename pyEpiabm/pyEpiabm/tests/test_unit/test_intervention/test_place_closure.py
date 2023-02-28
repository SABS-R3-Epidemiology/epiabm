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
        """Intialise a population with one cell and one microcell with
        one infector.
        """
        super(TestPlaceClosure, cls).setUpClass()  # Sets up parameters
        cls.time = 1
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._microcell = cls._population.cells[0].microcells[0]
        cls._microcell.add_people(1)
        cls._microcell.persons[0].update_status(InfectionStatus(7))

        params = pe.Parameters.instance().intervention_params['place_closure']
        cls.placeclosure = PlaceClosure(population=cls._population, **params)

    def test__init__(self):
        self.assertEqual(self.placeclosure.start_time, 6)
        self.assertEqual(self.placeclosure.policy_duration, 365)
        self.assertEqual(self.placeclosure.case_threshold, 0)
        self.assertEqual(self.placeclosure.closure_delay, 0)
        self.assertEqual(self.placeclosure.closure_duration, 100)
        self.assertEqual(self.placeclosure.icu_microcell_threshold, 1)
        self.assertEqual(self.placeclosure.case_microcell_threshold, 1)

    def test___call__(self):
        self.assertIsNone(self._microcell.closure_start_time)
        self.placeclosure(time=5)
        self.assertIsNotNone(self._microcell.closure_start_time)
        self.placeclosure(time=150)
        self.assertIsNone(self._microcell.closure_start_time)

    def test__turn_off__(self):
        self._microcell.closure_start_time = 370
        self.placeclosure.__turn_off__()
        self.assertIsNone(self._microcell.closure_start_time)


if __name__ == '__main__':
    unittest.main()
