import unittest

import pyEpiabm as pe
from pyEpiabm.sweep import TravelSweep
from pyEpiabm.property import InfectionStatus
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestTravelSweep(TestPyEpiabm):
    """Test the 'TravelSweep' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super(TestTravelSweep, cls).setUpClass()
        cls.travelsweep = TravelSweep()

        # Construct a population with 20 individuals in 1 cells,
        # 2 microcells and 4 households with 2 infectors.
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.pop_params = {"population_size": 20, "cell_number": 1,
                          "microcell_number": 2, "household_number": 4}
        cls._population = cls.pop_factory.make_pop(cls.pop_params)
        for person in cls._population.cells[0].persons:
            person.update_status(InfectionStatus(1))
        initial_infected_person1 = cls._population.cells[0].microcells[0].persons[0]
        initial_infected_person1.update_status(InfectionStatus(4))
        initial_infected_person2 = cls._population.cells[0].microcells[1].persons[0]
        initial_infected_person2.update_status(InfectionStatus(4))

        cls.travelsweep.bind_population(cls._population)

    def test_bind_population(self):
        self.assertEqual(len(self.travelsweep.
                             travel_params), 2)
        self.test_sweep = pe.sweep.TravelSweep()
        self.test_sweep.bind_population(self._population)
        self.assertEqual(self.test_sweep._population.cells[0]
                         .persons[0].infection_status,
                         pe.property.InfectionStatus.InfectMild)

    def test__call__(self):
        self.travelsweep.travel_params['ratio_introduce_cases'] = 1.0
        self.travelsweep(time=1)
        self.assertEqual(len(self._population.cells[0].persons), 22)
        for person in self._population.cells[0].persons:
            if (hasattr(person, 'travel_end_time')):
                print(person.travel_end_time)
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.0
        # self.travelsweep(time=10)
        # print(len(self._population.cells[0].persons))
        self.travelsweep(time=16)
        self.travelsweep(time=14)
        # self.assertEqual(len(self._population.cells[0].persons), 20)
        print(self.travelsweep.travel_params['ratio_introduce_cases'])
        for person in self._population.cells[0].persons:
            if (hasattr(person, 'travel_end_time')):
                print(person.travel_end_time)

    # def create_introduced_individuals(self):

    # def test_check_leaving_individuals(self):
    #     self.test_sweep = pe.sweep.TravelSweep()
    #     self.travelsweep.travel_params['ratio_introduce_cases'] = 1.0
    #     self.travelsweep(time=1)
    #     print(self.test_sweep.introduce_population.cells[0].persons)


if __name__ == '__main__':
    unittest.main()