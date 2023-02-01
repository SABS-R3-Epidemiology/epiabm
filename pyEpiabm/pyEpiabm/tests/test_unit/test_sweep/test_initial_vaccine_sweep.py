import unittest

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm

class TestVaccinationSweep(TestPyEpiabm):
    """ Tests the initial vaccine sweep class in which a vaccination
    queue is generated.
    """

    def setUp(cls) -> None:
        """Sets up a population we can use throughout the test.
        2 people are located in one microcell.
        """
        super(TestVaccinationSweep, cls).setUp()
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 6, "cell_number": 1,
                          "microcell_number": 1, "household_number": 1}
        cls.test_population = cls.pop_factory.make_pop(cls.pop_params)
        cls.cell = cls.test_population.cells[0]
        cls.microcell = cls.cell.microcells[0]
        cls.person1 = cls.cell.microcells[0].persons[0]
        cls.person2 = cls.test_population.cells[0].microcells[0].persons[1]
        cls.person3 = cls.test_population.cells[0].microcells[0].persons[2]
        cls.person4 = cls.test_population.cells[0].microcells[0].persons[3]
        cls.person5 = cls.test_population.cells[0].microcells[0].persons[4]
        cls.person6 = cls.test_population.cells[0].microcells[0].persons[5]

    def test_priority_group(self):
        test_sweep = pe.sweep.InitialVaccineQueue()
        test_sweep.bind_population(self.test_population)
        params = pe.Parameters.instance().intervention_params['vaccine_params']
        
        self.person1.age = 90
        self.person2.age = 70
        self.person3.age = 55
        self.person4.age = 30
        self.person5.age = 15
        self.person6.care_home_resident = True

        person_list = [self.person1, self.person2, self.person3, 
                       self.person4, self.person5, self.person6]
        for per in person_list:
            test_sweep.assign_priority_group(per, params['min_ages'])
        
        self.assertEqual(self.person1.priority_level, 1)
        self.assertEqual(self.person6.priority_level, 1)
        self.assertEqual(self.person2.priority_level, 2)
        self.assertEqual(self.person3.priority_level, 3)
        self.assertEqual(self.person4.priority_level, 4)
        self.assertIsNone(self.person5.priority_level)


if __name__ == '__main__':
    unittest.main()
