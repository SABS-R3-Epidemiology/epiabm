import unittest
import numpy as np

import pyEpiabm as pe
from pyEpiabm.core import Parameters
from pyEpiabm.sweep import TravelSweep
from pyEpiabm.property import InfectionStatus
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestTravelSweep(TestPyEpiabm):
    """Test the 'TravelSweep' class.
    """

    def setUp(self) -> None:
        super(TestTravelSweep, self).setUp()
        self.travelsweep = TravelSweep()

        # Construct a population with 20 individuals in 1 cells,
        # 2 microcells and 4 households with 2 infectors.
        self._population = pe.Population()
        self._population.add_cells(1)
        self.cell = self._population.cells[0]
        self._population.cells[0].add_microcells(2)
        self.microcell1 = self.cell.microcells[0]
        self.microcell2 = self.cell.microcells[1]
        self.microcell1.add_people(15)
        self.microcell2.add_people(5)
        self.microcell1.add_household(self.microcell1.persons.copy()[:10])
        self.microcell1.add_household(self.microcell1.persons.copy()[10:])
        self.microcell2.add_household(self.microcell1.persons.copy()[:3])
        self.microcell2.add_household(self.microcell1.persons.copy()[3:])
        # By default all susceptible, make 2 infectious
        self.initial_infected_person1 = self.microcell1.persons[0]
        self.initial_infected_person1.update_status(InfectionStatus(4))
        self.initial_infected_person2 = self.microcell2.persons[0]
        self.initial_infected_person2.update_status(InfectionStatus(4))

        self.travelsweep.bind_population(self._population)

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
        # using age
        Parameters.instance().use_ages = 1
        Parameters.instance().age_proportions = np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0])
        Parameters.instance().host_progression_lists[
            "prob_exposed_to_asympt"] = [1.0]*17
        self.test_sweep = pe.sweep.TravelSweep()
        self.test_sweep.create_introduced_idividuals(
            time=1, number_individuals_introduced=2)
        self.assertEqual(len(self.test_sweep.initial_microcell.persons), 2)
        for person in self.test_sweep.initial_microcell.persons:
            # Both in age_group 5, age between 25-30 years and InfectAsymp
            self.assertEqual(person.age_group, 5)
            self.assertTrue(person.age >= 25 and person.age < 30)
            self.assertEqual(person.infection_status,
                             InfectionStatus.InfectASympt)
        # not using age
        Parameters.instance().use_ages = False
        Parameters.instance().host_progression_lists[
            "prob_exposed_to_asympt"] = [1.0]*17
        self.test_sweep = pe.sweep.TravelSweep()
        self.test_sweep.create_introduced_idividuals(
            time=1, number_individuals_introduced=2)
        self.assertEqual(len(self.test_sweep.initial_microcell.persons), 2)
        for person in self.test_sweep.initial_microcell.persons:
            self.assertEqual(person.age, None)
            self.assertEqual(person.infection_status,
                             InfectionStatus.InfectASympt)

    def test_assign_microcell_household(self):
        # Introduce one individual to microcell with highest population density
        # starting own household.
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.5
        self.travelsweep.travel_params['prob_existing_household'] = 0.0
        self.assertEqual(len(self.microcell1.persons), 15)
        self.assertEqual(len(self.microcell1.households), 2)
        self.travelsweep(time=1)
        self.assertEqual(len(self.microcell1.persons), 16)
        self.assertEqual(len(self.microcell1.households), 3)

    def test_remove_leaving_individual(self):
        # Don't introduce new person, remove existing
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.0
        self.initial_infected_person1.travel_end_time = 10
        self.travelsweep(time=10)
        self.assertEqual(len(self._population.cells[0].persons), 20)
        self.travelsweep(time=11)
        self.assertEqual(len(self._population.cells[0].persons), 19)

        # Remove after end time and isolation and quarantine over
        self.initial_infected_person2.travel_end_time = 20
        self.initial_infected_person2.isolation_start_time = 23
        self.initial_infected_person2.quarantine_start_time = 24
        self.travelsweep(time=21)
        self.assertEqual(len(self._population.cells[0].persons), 19)
        self.travelsweep(time=23)
        self.assertEqual(len(self._population.cells[0].persons), 19)
        self.travelsweep(time=24)
        self.assertEqual(len(self._population.cells[0].persons), 18)

        # Remove after end time and isolation is over
        self.microcell1.persons[1].travel_end_time = 25
        self.microcell1.persons[1].isolation_start_time = 27
        self.travelsweep(time=25)
        self.assertEqual(len(self._population.cells[0].persons), 18)
        self.travelsweep(time=27)
        self.assertEqual(len(self._population.cells[0].persons), 17)

        # Remove after end time and quarantine is over
        self.microcell1.persons[2].travel_end_time = 28
        self.microcell1.persons[2].quarantine_start_time = 30
        self.travelsweep(time=28)
        self.assertEqual(len(self._population.cells[0].persons), 17)
        self.travelsweep(time=30)
        self.assertEqual(len(self._population.cells[0].persons), 16)


if __name__ == '__main__':
    unittest.main()
