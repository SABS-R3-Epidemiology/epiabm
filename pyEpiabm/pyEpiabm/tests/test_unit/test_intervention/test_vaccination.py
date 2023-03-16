import unittest

import pyEpiabm as pe
from pyEpiabm.intervention import Vaccination
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestVaccination(TestPyEpiabm):
    """ Test the 'Vaccination' class
    """

    def setUp(self) -> None:
        super(TestVaccination, self).setUp()  # Sets up patch on logging

        # Construct a population with 5 persons
        self._population = pe.Population()
        self._population.add_cells(1)
        self._population.cells[0].add_microcells(1)
        self._population.cells[0].microcells[0].add_people(5)
        if isinstance(pe.Parameters.instance().
                      intervention_params['vaccine_params'], list):
            pe.Parameters.instance().intervention_params['vaccine_params'] = \
                pe.Parameters.instance().intervention_params[
                    'vaccine_params'][0]
        self.params = pe.Parameters.instance().\
            intervention_params['vaccine_params']
        self.vaccination = Vaccination(**self.params,
                                       population=self._population
                                       )

        ages = [90, 70, 55, 30, 15]
        for i in range(5):
            person = self._population.cells[0].microcells[0].persons[i]
            person.age = ages[i]

        self.person_90_yo = self._population.cells[0].persons[0]

        test_sweep = pe.sweep.InitialVaccineQueue()
        test_sweep.bind_population(self._population)
        for per in self._population.cells[0].microcells[0].persons:
            test_sweep.assign_priority_group(per, self.params['min_ages'])
        test_sweep.__call__(None)

    def test_enqueue(self):
        # test all 4 people over 18 were added to vaccination queue
        self.assertEqual(self._population.vaccine_queue.qsize(), 4)
        # check the first person in the queue is the 90 year old
        # queue[0][2] takes the data stored in the first element of the queue
        self.assertEqual(self._population.vaccine_queue.queue[0][2],
                         self.person_90_yo)

    def test__init__(self):
        self.assertEqual(self.vaccination.daily_doses,
                         self.params['daily_doses'])
        self.assertEqual(self.vaccination.start_time,
                         self.params['start_time'])
        self.assertEqual(self.vaccination.policy_duration,
                         self.params['policy_duration'])
        self.assertEqual(self.vaccination.case_threshold,
                         self.params['case_threshold'])

    def test__call__(self):
        self.vaccination(time=5)
        self.assertEqual(self._population.vaccine_queue.qsize(), 3)
        self.assertTrue(self.person_90_yo
                        not in self._population.vaccine_queue.queue)
        self.assertTrue(self.person_90_yo.is_vaccinated)
        self.assertEqual(self.person_90_yo.date_vaccinated, 5)


if __name__ == '__main__':
    unittest.main()
