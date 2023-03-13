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
        """Construct a population with 20 individuals in 1 cells,
        2 microcells and 4 households with 2 infectors. Note,
        ratio_introduce_cases can be used to introduce a certain
        number of individuals.

        """
        super(TestTravelSweep, self).setUp()
        self.travelsweep = TravelSweep()

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
        self.travelsweep.travel_params['constant_introduce_cases'] = [0]

        self.travelsweep.bind_population(self._population)

    def test_bind_population(self):
        self.assertEqual(len(self.travelsweep.
                             travel_params), 4)
        self.test_sweep = pe.sweep.TravelSweep()
        self.test_sweep.bind_population(self._population)
        self.assertEqual(self.test_sweep._population.cells[0]
                         .persons[0].infection_status,
                         pe.property.InfectionStatus.InfectMild)

    def test__call__(self):
        """Introduce 3 infected individuals. Of them, 2 are introduced due to
        ratio_introduce_cases and 1 due to constant_introduce_cases. All
        three individuals stay until a day between day 3 and 15. Introduce 0
        individuals at day 2 and remove the 3 individuals after their
        travel_end_time has passed. Set ratio_introduced_cases to zero after
        introducing these 2 individuals to prevent introducing more
        individuals and check if the population size is as expected at the
        considered time points.

        """
        self.travelsweep.travel_params['ratio_introduce_cases'] = 1.0
        self.travelsweep.travel_params['constant_introduce_cases'] = [1]
        self.travelsweep.travel_params['duration_travel_stay'] = [2, 14]
        self.travelsweep(time=1)
        self.assertEqual(len(self._population.cells[0].persons), 23)
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.0
        self.travelsweep.travel_params['constant_introduce_cases'] = [1, 1, 0]
        self.travelsweep(time=2)
        self.travelsweep.travel_params['constant_introduce_cases'] = [0]
        self.travelsweep(time=16)
        self.assertEqual(len(self._population.cells[0].persons), 20)

    def test_create_introduced_individuals(self):
        """Create Person objects for the two infected individuals introduced
        with and without using age in the model. When using age, their
        age_group should be 5 and they should be asymptomatic. When age is not
        used, their age should be None and they should still be asymptomatic.

        """
        # Using age
        Parameters.instance().use_ages = 1
        Parameters.instance().age_proportions = np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0])
        Parameters.instance().host_progression_lists[
            "prob_exposed_to_asympt"] = [1.0]*17
        self.travelsweep.travel_params['duration_travel_stay'] = [2, 2]
        self.test_sweep = pe.sweep.TravelSweep()
        self.test_sweep.create_introduced_individuals(
            time=1, number_individuals_introduced=2)
        self.assertEqual(len(self.test_sweep.initial_microcell.persons), 2)
        for person in self.test_sweep.initial_microcell.persons:
            # Both staying 1+2=3 days, in age_group 5, age between 25-30 years,
            # and infectionstatus is asymptomatic.
            self.assertEqual(person.travel_end_time, 3)
            self.assertEqual(person.age_group, 5)
            self.assertTrue(person.age >= 25 and person.age < 30)
            self.assertEqual(person.infection_status,
                             InfectionStatus.InfectASympt)
        # Not using age
        Parameters.instance().use_ages = False
        Parameters.instance().host_progression_lists[
            "prob_exposed_to_asympt"] = [1.0]*17
        self.test_sweep = pe.sweep.TravelSweep()
        self.test_sweep.create_introduced_individuals(
            time=1, number_individuals_introduced=2)
        self.assertEqual(len(self.test_sweep.initial_microcell.persons), 2)
        for person in self.test_sweep.initial_microcell.persons:
            self.assertEqual(person.age, None)
            self.assertEqual(person.infection_status,
                             InfectionStatus.InfectASympt)

    def test_assign_microcell_household(self):
        """Introduce one individual and assign to the microcell with the
        highest population density. Individual starts their own household.

        """
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.5
        self.travelsweep.travel_params['prob_existing_household'] = 0.0
        self.travelsweep.travel_params['duration_travel_stay'] = [2, 2]

        self.assertEqual(len(self.microcell1.persons), 15)
        self.assertEqual(len(self.microcell1.households), 2)
        self.travelsweep(time=1)
        self.assertEqual(len(self.microcell1.persons), 16)
        self.assertEqual(len(self.microcell1.households), 3)

    def test_remove_leaving_individual(self):
        """Remove individuals introduced after their travel_end_time has
        passed and check if they are not in isolation and/or quarantine.
        If so, keep them in the population until isolation_start_time and/or
        quaratine_start_time has also passed. Check if the population size
        is as expected at the considered time points.

        """
        # Introduce one traveller staying for 2 days
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.5
        self.travelsweep.travel_params['duration_travel_stay'] = [2, 2]
        self.travelsweep(time=10)
        self.assertEqual(len(self._population.cells[0].persons), 21)
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.0
        self.travelsweep(time=13)
        self.assertEqual(len(self._population.cells[0].persons), 20)

        # Remove after end time and isolation and quarantine over
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.5
        self.travelsweep.travel_params['duration_travel_stay'] = [2, 2]
        # Introduce individual staying untill day 16
        self.travelsweep(time=14)
        introduced_person = self.cell.persons[-1]
        introduced_person.isolation_start_time = 18
        introduced_person.quarantine_start_time = 19
        introduced_person.travel_isolation_start_time = 18
        self.travelsweep.travel_params['ratio_introduce_cases'] = 0.0
        self.travelsweep(time=17)
        self.assertEqual(len(self._population.cells[0].persons), 21)
        self.travelsweep(time=18)
        self.assertEqual(len(self._population.cells[0].persons), 21)
        introduced_person.isolation_start_time = None
        introduced_person.quarantine_start_time = None
        self.travelsweep(time=22)
        self.assertEqual(len(self._population.cells[0].persons), 21)
        introduced_person.travel_isolation_start_time = None
        self.travelsweep(time=23)
        self.assertEqual(len(self._population.cells[0].persons), 20)


if __name__ == '__main__':
    unittest.main()
