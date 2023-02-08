import unittest

import pyEpiabm as pe
from pyEpiabm.intervention import Vaccination
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm

class TestVaccination(TestPyEpiabm):
    """ Test the 'Vaccination' class
        This class takes people from the queue and vaccinates them.
    """
    
    def setUp(cls) -> None:
        super(TestVaccination, cls).setUp()  # Sets up patch on logging

        # Construct a population with 5 persons
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._population.cells[0].microcells[0].add_people(5)
        params = pe.Parameters.instance().intervention_params['vaccine_params']
        cls.vaccination = Vaccination(**params,
                                      population = cls._population
                                      )

        ages = [90, 70, 55, 30, 15]
        for i in range(5):
            person = cls._population.cells[0].microcells[0].persons[i]
            person.age = ages[i]

        test_sweep = pe.sweep.InitialVaccineQueue()
        test_sweep.bind_population(cls._population)
        for per in cls._population.cells[0].microcells[0].persons:    
            test_sweep.assign_priority_group(per, params['min_ages'])
        test_sweep.__call__(None)

    def test_enqueue(self):
        self.assertEqual(self._population.vaccine_queue.qsize(), 4)
        self.assertEqual(self._population.vaccine_queue.queue[0][2], self._population.cells[0].persons[0])

    def test__init__(self):
        self.assertEqual(self.vaccination.daily_doses, 1)
        self.assertEqual(self.vaccination.start_time, 6)
        self.assertEqual(self.vaccination.policy_duration, 365)
        self.assertEqual(self.vaccination.case_threshold, 0)
    
    def test__call__(self):
        self.vaccination(time=5)
        self.assertEqual(self._population.vaccine_queue.qsize(), 3)
        self.assertTrue(self._population.cells[0].persons[0] not in self._population.vaccine_queue.queue)
        self.assertTrue(self._population.cells[0].persons[0].is_vaccinated)
        self.assertEqual(self._population.cells[0].persons[0].date_vaccinated, 5)

    
if __name__ == '__main__':
   unittest.main()
