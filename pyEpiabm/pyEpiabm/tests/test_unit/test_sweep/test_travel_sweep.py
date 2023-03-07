import unittest

import pyEpiabm as pe
from pyEpiabm.core import Parameters
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
        initial_infected_person1 = \
            cls._population.cells[0].microcells[0].persons[0]
        initial_infected_person1.update_status(InfectionStatus(4))
        initial_infected_person2 = \
            cls._population.cells[0].microcells[1].persons[0]
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
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.0
        self.travelsweep(time=16)
        self.assertEqual(len(self._population.cells[0].persons), 20)

    def test_create_introduced_individuals(self):
        Parameters.instance().use_ages = 1
        Parameters.instance().age_proportions = \
            [0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0]
        Parameters.instance().host_progression_lists[
            "prob_exposed_to_asympt"] = 1.0
        self.test_sweep = pe.sweep.TravelSweep()
        self.test_sweep.create_introduced_idividuals(
            time=1, number_individuals_introduced=2)
        print(self.test_sweep.initial_microcell.persons)
        self.assertEqual(len(self.test_sweep.initial_microcell.persons), 2)


if __name__ == '__main__':
    unittest.main()
