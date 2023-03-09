import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestVaccinationSweep(TestPyEpiabm):
    """ Tests the initial vaccine sweep class in which a vaccination
    queue is generated.
    """

    def setUp(self) -> None:
        """Sets up a population we can use throughout the test.
        6 people are located in one microcell.
        """
        super(TestVaccinationSweep, self).setUp()
        self.pop_factory = pe.routine.ToyPopulationFactory()
        self.pop_params = {"population_size": 6, "cell_number": 1,
                           "microcell_number": 1, "household_number": 1}
        self.test_population = self.pop_factory.make_pop(self.pop_params)
        self.cell = self.test_population.cells[0]
        self.microcell = self.cell.microcells[0]
        self.person_list = []
        for i in range(6):
            self.person_list.append(self.microcell.persons[i])

    def test_priority_group(self):
        test_sweep = pe.sweep.InitialVaccineQueue()
        test_sweep.bind_population(self.test_population)
        params = pe.Parameters.instance().intervention_params['vaccine_params']

        age_list = [90, 70, 55, 30, 15, 80]
        for i in range(len(self.person_list)):
            self.person_list[i].age = age_list[i]

        self.person_list[5].care_home_resident = True

        priority_list = []
        for per in self.person_list:
            level = test_sweep.assign_priority_group(per, params['min_ages'])
            priority_list.append(level)

        self.assertEqual(priority_list[0], 1)
        self.assertEqual(priority_list[5], 1)
        self.assertEqual(priority_list[1], 2)
        self.assertEqual(priority_list[2], 3)
        self.assertEqual(priority_list[3], 4)
        self.assertIsNone(priority_list[4])

    @mock.patch("pyEpiabm.core.Parameters.instance")
    @mock.patch("logging.error")
    def test_warning(self, mock_log, mock_params):
        mock_params.return_value.intervention_params = {}
        pe.sweep.InitialVaccineQueue()
        mock_log.assert_called_once()


if __name__ == '__main__':
    unittest.main()
